"""Replay application thresholds over real saved responses; never runs a model."""

import argparse
import json
from pathlib import Path
from common import route, summarize, workload


def load_records(path):
    result = json.loads(Path(path).read_text())
    expected = {t["id"]: t["expected"] for t in workload()["tickets"]}
    records = result["records"]
    if not records or len({r["id"] for r in records}) != len(records):
        raise ValueError("A run needs at least one record and unique ticket IDs")
    for r in records:
        if r["id"] not in expected or r["expected"] != expected[r["id"]]:
            raise ValueError("Run labels do not match this teaching workload")
    return result, records


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run")
    parser.add_argument("--thresholds", type=float, nargs="+", default=[0.5, 0.8, 0.9])
    args = parser.parse_args()
    result, records = load_records(args.run)
    print("Backend:", result["backend"], "| Saved predictions:", len(records))
    for threshold in args.thresholds:
        replay = [dict(r, policy=route(r["response"], threshold)) for r in records]
        print(json.dumps({"threshold": threshold, **summarize(replay)}, indent=2))


if __name__ == "__main__":
    main()
