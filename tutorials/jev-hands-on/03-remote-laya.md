# 3. Run an independent open model on a remote GPU

[Previous: routing and evaluation](02-routing-and-evaluation.md) · [Back to the tutorial](README.md) · [Experiment notes](RESULTS.md)

This lesson runs the same support questions with [Laya](https://github.com/NandhaKishorM/laya) [![GitHub stars](https://img.shields.io/github/stars/NandhaKishorM/laya?style=flat-square&label=%E2%98%85)](https://github.com/NandhaKishorM/laya), an independent model/runtime, using its [public English checkpoint](https://huggingface.co/convaiinnovations/laya). The weights are not official Jev weights. Check the publisher's license and model card when choosing a checkpoint.

The experiment needs one CUDA GPU. Run it on a Linux server; keep the Mac for editing, policy tests, and reading results. The runner rejects macOS, missing CUDA, and configurations exposing more than one GPU.

## Prepare separate code and data directories

On your authorized server, choose a small-file directory and a large-data directory. For this exercise, the small-file directory was a new child under `ScienceIDE`; the checkpoint and environment were placed on `/data3`. Use paths appropriate to your server, not another project's directories.

```bash
export JEV_CODE_DIR="$HOME/jev-hands-on"
export JEV_DATA_DIR="/data3/jev-hands-on"
mkdir -p "$JEV_CODE_DIR" "$JEV_DATA_DIR"
df -h "$JEV_CODE_DIR" "$JEV_DATA_DIR"
```

Copy this tutorial's `.py` files, `workload.json`, `questions-concise.json`, and `requirements-gpu.txt` into the code directory. Keep local checkpoint manifests, `.venv`, `.work`, `results`, and `runs` out of the copy. Keep raw run logs in the small-file directory, and downloaded weights and package caches on the large-data disk.

## Create an environment on the server

The tested inference stack used Python 3.12.14, PyTorch 2.6.0+cu118, Transformers 4.52.4, NumPy 1.26.4, and Laya 0.3.24. A fresh environment with Python 3.12 can be installed as follows:

```bash
python3.12 -m venv "$JEV_DATA_DIR/venv"
source "$JEV_DATA_DIR/venv/bin/activate"
export PIP_CACHE_DIR="$JEV_DATA_DIR/pip-cache"
python -m pip install torch==2.6.0 \
  --index-url https://download.pytorch.org/whl/cu118
cd "$JEV_CODE_DIR"
python -m pip install -r requirements-gpu.txt
python -c 'import torch, laya; print(torch.__version__, laya.__version__, torch.cuda.is_available())'
```

The CUDA wheel command comes from the [official PyTorch version instructions](https://pytorch.org/get-started/previous-versions/#v260). Driver compatibility still needs to be checked on your server. A CPU-only wheel is not suitable for this timing exercise.

In our actual run, a verified existing CUDA environment supplied immutable dependencies through an explicit site-packages path in the new environment; Laya was installed only into the new environment. We did not perform the fresh-install sequence above on that server. A nested `venv --system-site-packages` initially failed to find PyTorch: it does not reliably inherit the packages of the intermediate virtual environment. For a beginner, a fresh environment is easier to reproduce than that dependency-sharing workaround.

## Select an idle GPU immediately before running

```bash
nvidia-smi --query-gpu=index,name,memory.used,memory.total,utilization.gpu \
  --format=csv
```

Check the occupancy and any server scheduling rules. Export the physical index of one available card, for example:

```bash
export CUDA_VISIBLE_DEVICES=2
```

The example index is from our observed run, not a reservation or a recommendation to always use GPU 2. We initially found GPU 0 idle, but another task occupied it before launch; we rechecked and selected GPU 2. Inside the process, the selected physical card appears as logical CUDA device 0. Do not interrupt other users' processes.

## Pin the checkpoint and run the workload

```bash
export HF_HOME="$JEV_DATA_DIR/hub"
python run_laya.py --output runs/laya.json
python evaluate.py runs/laya.json --thresholds 0.5 0.8 0.9
du -sh "$JEV_DATA_DIR" "$JEV_CODE_DIR/runs"
```

For the documented wording comparison, keep the original run and write a second file:

```bash
python run_laya.py --questions questions-concise.json \
  --output runs/laya-concise.json
```

The runner pins commit `55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851` and verifies the five file hashes in `EXPECTED_SHA256` in [run_laya.py](run_laya.py) before loading. This English checkpoint consists of one ~843 MB weight file plus small encoder/tokenizer configuration files. Laya's filtered download avoids fetching the multilingual and typed-decisions sibling checkpoints.

If the verified files have already been transferred to a local server directory, the tested offline invocation is:

```bash
export HF_HUB_OFFLINE=1
export TRANSFORMERS_OFFLINE=1
python run_laya.py --checkpoint "$JEV_DATA_DIR/checkpoint" \
  --output runs/laya.json
```

The same hashes apply to this local directory. Keep a clean copy of publisher files when preparing another run: some runtime versions normalize tokenizer configuration while loading. If a later integrity check fails, investigate the changed file and restore the original pinned artifact rather than changing the expected hash to accept an unknown file.

The weight hash can also be inspected in the [publisher's file record](https://huggingface.co/convaiinnovations/laya/blob/main/model.safetensors). Our download used an HTTPS mirror as a transport because direct resolution failed, then checked its pinned file manifest and the weight's SHA256 against the original publisher record. We streamed the weight to the server; no model inference occurred on the Mac. Neither endpoint used disabled certificate checks.

## Understand the measurements

The script loads one model, runs one warm-up request, and then executes twelve sequential requests containing three questions each. CUDA synchronization brackets each measured request. It records model-load time, the median warm request time, peak PyTorch allocated/reserved GPU memory, dependency versions, and a CPU-fallback count.

Warm timings exclude download, model loading, and the first request. They include tokenization, inference, and conversion into returned answers. They are a measurement of this workload on this server, not an API latency comparison or a throughput benchmark. Peak PyTorch allocation excludes driver/context memory and may differ from `nvidia-smi`.

## Lessons from the environment

| Problem | Resolution used in this exercise |
| --- | --- |
| Shared default Python had a NumPy/PyTorch ABI incompatibility | Used a separate environment with a verified compatible stack; did not downgrade the shared environment |
| Nested virtual environment could not import PyTorch | Explicitly linked the verified dependency directory for this run; document the workaround rather than imply a fresh install |
| Direct model hostname could not resolve | Downloaded pinned files through a working HTTPS transport and verified their hashes |
| Remote endpoint returned a certificate mismatch | Kept TLS verification enabled and transferred verified files from a working network path |
| Planned GPU became occupied | Rechecked occupancy and selected another idle card |
| CPU fallback could invalidate GPU measurements | Checked the actual device and fallback counter; refuse such a timing run |

Read [RESULTS.md](RESULTS.md) for the actual predictions and limitations. Laya's Choice/Score `confidence` uses normalized entropy in the tested runtime, while official Jev documents different formulas. Laya also exposes `answer_confidence` and action metadata; our shared teaching policy does not consume those fields. The same numerical policy threshold should not be treated as equivalent certainty across these backends. See the [runtime's implementation](https://github.com/NandhaKishorM/laya/blob/main/laya/common.py) when selecting a measure for your own application.
