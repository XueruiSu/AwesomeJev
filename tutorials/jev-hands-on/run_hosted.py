"""Run the synthetic teaching cases against the official hosted Jev API."""

import argparse
import datetime
import getpass
import importlib.metadata
import json
import os
from pathlib import Path
import time
from common import route, summarize, workload


def build_questions(data):
    from typesafe_sdk import Choice, Noul, Score
    constructors = {"choice": Choice, "score": Score, "noul": Noul}
    return {k: constructors[q["type"]](**{f: v for f, v in q.items() if f != "type"}) for k, q in data["questions"].items()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, default=1, help="Start with one ticket; the corpus contains twelve")
    parser.add_argument("--model", default="jev-1.13.0")
    parser.add_argument("--output", default="runs/hosted.json")
    parser.add_argument("--prompt-key", action="store_true", help="Read the API key without echoing or saving it")
    args = parser.parse_args()
    if not 1 <= args.limit <= 12:
        parser.error("--limit must be between 1 and 12")
    if args.prompt_key:
        os.environ["TYPESAFE_API_KEY"] = getpass.getpass("TypeSafe API key: ").strip()
    if not os.environ.get("TYPESAFE_API_KEY"):
        parser.error("Set TYPESAFE_API_KEY locally. Do not paste it into source files or chat.")
    from typesafe_sdk import RetryPolicy, TypeSafeClient, TypeSafeError
    data = workload()
    questions = build_questions(data)
    records = []
    failure = None
    with TypeSafeClient(model=args.model, timeout=30, retry=RetryPolicy(max_retries=0)) as client:
        for ticket in data["tickets"][:args.limit]:
            started = time.perf_counter()
            try:
                response = client.system_one(state=ticket["text"], questions=questions).model_dump(mode="json")
            except TypeSafeError as exc:
                # Persist an explicit failure, never a fabricated model answer.
                failure = type(exc).__name__
                response = None
            elapsed = (time.perf_counter() - started) * 1000
            records.append({"id": ticket["id"], "expected": ticket["expected"], "response": response, "policy": route(response), "elapsed_ms": elapsed})
            if failure:
                records[-1]["error_type"] = failure
            print(ticket["id"], records[-1]["policy"])
            if failure:
                break
    result = {"backend": "official-hosted-jev", "run_date": datetime.datetime.now(datetime.timezone.utc).isoformat(), "sdk_version": importlib.metadata.version("typesafe-sdk"), "requested_model": args.model, "requested_tickets": args.limit, "completed": failure is None, "error_type": failure, "summary": summarize(records), "records": records}
    path = Path(args.output); path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result["summary"], indent=2))
    if failure:
        raise SystemExit("Stopped after " + failure + "; see the hosted tutorial's troubleshooting table.")


if __name__ == "__main__":
    main()
