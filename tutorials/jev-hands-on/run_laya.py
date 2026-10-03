"""Run independent open-model inference on a remote CUDA GPU, never on this Mac."""

import argparse
import datetime
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import statistics
import time
from common import route, summarize, workload

REVISION = "55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkpoint", default="convaiinnovations/laya")
    parser.add_argument("--revision", default=REVISION)
    parser.add_argument("--output", default="runs/laya.json")
    parser.add_argument("--questions", help="Optional JSON question set; keep the same answer keys and rubric")
    args = parser.parse_args()
    if platform.system() == "Darwin":
        parser.error("Run this model experiment on a remote CUDA server, not on macOS.")
    visible = os.environ.get("CUDA_VISIBLE_DEVICES", "")
    if not visible or len(visible.split(",")) != 1:
        parser.error("Select exactly one currently free GPU with CUDA_VISIBLE_DEVICES.")
    if not os.environ.get("HF_HOME"):
        parser.error("Set HF_HOME to a dedicated cache on the large-data disk.")
    import torch
    import laya
    if not torch.cuda.is_available():
        parser.error("A working CUDA runtime is required; CPU fallback is not this experiment.")
    torch.manual_seed(0)
    data = workload()
    if args.questions:
        data["questions"] = json.loads(Path(args.questions).read_text())
    started = time.perf_counter()
    manifest = json.loads((Path(__file__).parent / "checkpoint.json").read_text())
    if args.revision != manifest["revision"]:
        parser.error("This teaching experiment verifies one pinned revision; update checkpoint.json for another.")
    agent = laya.load(args.checkpoint, device="cuda", revision=args.revision,
                      expected_sha256=manifest["sha256"])
    load_seconds = time.perf_counter() - started
    if not str(agent.device).startswith("cuda"):
        raise RuntimeError("The model did not load on CUDA")
    agent.predict(data["tickets"][0]["text"], data["questions"])
    torch.cuda.synchronize(); torch.cuda.reset_peak_memory_stats()
    records = []
    for ticket in data["tickets"]:
        torch.cuda.synchronize(); started = time.perf_counter()
        response = agent.predict(ticket["text"], data["questions"])
        torch.cuda.synchronize(); elapsed = (time.perf_counter() - started) * 1000
        if not str(agent.device).startswith("cuda"):
            raise RuntimeError("CPU fallback occurred; this is not a valid GPU timing run")
        records.append({"id": ticket["id"], "expected": ticket["expected"], "response": response, "policy": route(response), "elapsed_ms": elapsed})
        print(ticket["id"], records[-1]["policy"], f"{elapsed:.1f} ms", flush=True)
    if agent.cpu_fallback_count:
        raise RuntimeError("CPU fallback occurred; this is not a valid GPU timing run")
    result = {
        "backend": "independent-laya", "run_date": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "checkpoint": args.checkpoint, "revision": args.revision,
        "questions": data["questions"],
        "versions": {p: importlib.metadata.version(p) for p in ("laya", "torch", "transformers", "huggingface-hub", "numpy")},
        "gpu": torch.cuda.get_device_name(0), "visible_device": visible,
        "cpu_fallback_count": agent.cpu_fallback_count,
        "load_seconds": load_seconds, "median_warm_request_ms": statistics.median(r["elapsed_ms"] for r in records),
        "peak_allocated_mib": torch.cuda.max_memory_allocated() / (1024 ** 2),
        "peak_reserved_mib": torch.cuda.max_memory_reserved() / (1024 ** 2),
        "summary": summarize(records), "records": records,
    }
    path = Path(args.output); path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k != "records"}, indent=2), flush=True)


if __name__ == "__main__":
    main()
