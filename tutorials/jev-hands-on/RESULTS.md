# Experiment notes: what actually ran

[Back to the tutorial](README.md)

**[2026-10-03]** These results cover twelve synthetic tickets evaluated with an independent Laya checkpoint on one remote RTX 3090. They are an observed teaching exercise, not a Jev benchmark or a calibration study.

## Evidence status

| Component | Evidence |
| --- | --- |
| Local application policy | Five offline tests passed on the Mac, using hand-written fixtures |
| Official SDK 0.7.2 | Four additional offline HTTP-transport tests passed; actual request encoding, response parsing, and failed-run recording exercised |
| Official hosted Jev | **Live evaluation pending: no TypeSafe API key was configured.** No hosted predictions or latency claims are reported |
| Independent Laya | Two completed remote GPU runs, twelve tickets each; measured summary and selected predictions documented below |
| Mac model inference | None; the GPU runner's macOS guard was exercised and rejected execution before model imports |

The official client tutorial is runnable once account access is configured. Its offline SDK checks are not evidence of live hosted behavior.

## Reproducible artifacts

| Artifact | Content |
| --- | --- |
| [workload.json](workload.json) | Original questions, tickets, and expected labels |
| [questions-concise.json](questions-concise.json) | One revised question set, written after inspecting the first run |
| [run_laya.py](run_laya.py) | Pinned checkpoint revision, expected file hashes, and run-file generation |

Run snapshots, checkpoint manifests, raw logs, environments, and working notes are retained locally and excluded from Git. The tables below preserve the measured summary and selected predictions from the two runs. To inspect complete responses or replay thresholds, generate local run files with the commands below.

## Environment and execution

Both runs used `convaiinnovations/laya` at commit `55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851`, Laya 0.3.24, Python 3.12.14, PyTorch 2.6.0+cu118, Transformers 4.52.4, Hugging Face Hub 0.36.2, NumPy 1.26.4, Safetensors 0.8.0, and Tokenizers 0.21.4. A verified local checkpoint was loaded with network access disabled during inference. Only one GPU was exposed, and no CPU fallback occurred.

For each run, one warm-up request preceded twelve measured sequential requests; each request contained the three questions. CUDA synchronization bracketed timing. No compilation or optional fast kernel was enabled. No training was performed. Runtime usage reported no dropped state tokens, no truncated questions, and no truncation for all 24 predictions.

The runtime emitted a warning that it clamped the checkpoint's `choice:11+` temperature from `0.10058` to `0.5`. Our Choice and Score questions have three options/levels, and Noul has two; the warned 11-or-more bucket was not used here. This warning still illustrates why package version and shipped calibration settings should be recorded.

| Observed metric | Original questions | Concise questions |
| --- | ---: | ---: |
| Valid outputs | 12 / 12 | 12 / 12 |
| Correct department | 5 / 12 | 11 / 12 |
| Correct refund-intent label at 0.5 | 11 / 12 | 12 / 12 |
| Urgency mean absolute error, 0–2 scale | 0.5341 | 0.4381 |
| Queued at policy threshold 0.8 | 0 / 12 | 0 / 12 |
| Median warm request time | 32.97 ms | 32.88 ms |
| Model-load time | 11.49 s | 9.49 s |
| Peak PyTorch allocated memory | 2322.11 MiB | 2319.18 MiB |
| Peak PyTorch reserved memory | 2516 MiB | 2518 MiB |

The large-data experiment directory used approximately **822 MiB** after the runs, excluding the pre-existing dependency environment reused read-only. Its small-file directory used approximately 404 KiB after both runs. The GPU was released when each process exited; after the first run, an inspection showed the selected card back at 5 MiB and 0% utilization. After both runs, no GPU process from this experiment remained. Other users subsequently occupied the card, and their jobs were left running. Freshly installing the full CUDA stack requires additional disk space; these figures are not fresh-install requirements.

## Inspect individual answers

The table shows predictions before the review policy. A valid but wrong category still counts as an error even when the policy sends it to review.

| Ticket | Expected department | Original prediction | Concise prediction | Expected urgency | Original score | Concise score |
| --- | --- | --- | --- | ---: | ---: | ---: |
| T01 | billing | billing | billing | 2 | 1.7195 | 1.8169 |
| T02 | billing | billing | billing | 0 | 0.8968 | 0.5927 |
| T03 | technical | other | technical | 2 | 1.9303 | 1.9414 |
| T04 | technical | other | technical | 1 | 1.0344 | 0.8531 |
| T05 | other | billing | other | 0 | 1.2996 | 0.9633 |
| T06 | billing | billing | billing | 0 | 0.2436 | 0.1449 |
| T07 | technical | other | technical | 2 | 1.8696 | 1.6350 |
| T08 | other | billing | technical | 1 | 0.9180 | 0.7613 |
| T09 | billing | billing | billing | 0 | 0.9729 | 0.4421 |
| T10 | billing | billing | billing | 0 | 1.2255 | 1.0505 |
| T11 | other | billing | other | 0 | 1.1074 | 1.0039 |
| T12 | technical | other | technical | 1 | 0.9332 | 0.9330 |

T06's refund probability changed from `0.4729` to `0.7624`, crossing the `0.5` label threshold. T09 correctly stayed below that threshold despite mentioning a refund. T10 selected billing in both runs despite its embedded instruction to classify as technical; it also received a much higher urgency score than the expected 0. These observations do not establish injection resistance or factual reliability.

## Question wording mattered in this exercise

The revised question set shortened instructions and gave concrete examples for the `other` category. We changed all three question descriptions together. Department results improved on the same twelve tickets, but this does not isolate which wording change caused the difference, and there was no independent validation set. The narrower examples for `other` also need expansion before using the revised criteria with new topics.

T08 remained wrong: a newsletter-address correction was classified as technical. Urgency still drifted above zero for requests with no stated deadline, such as T11. A useful next evaluation would include unseen topics, near-boundary urgency cases, and different wording for the same intent. Preserve the initial failures instead of reporting only the improved run.

Reproduce the two configurations on the remote server:

```bash
python run_laya.py --checkpoint "$JEV_DATA_DIR/checkpoint" \
  --output runs/laya.json
python run_laya.py --checkpoint "$JEV_DATA_DIR/checkpoint" \
  --questions questions-concise.json --output runs/laya-concise.json
```

Use the environment, GPU selection, and verified files from [lesson 3](03-remote-laya.md).

## Thresholds changed coverage, not predictions

After running the two configurations above, copy the generated `runs/` files from the server to your laptop and replay them with standard Python. The historical snapshot files are not included in the repository:

```bash
python evaluate.py runs/laya.json --thresholds 0 0.1 0.5 0.8 0.9
python evaluate.py runs/laya-concise.json --thresholds 0 0.1 0.5 0.8 0.9
```

| Policy threshold | Original queued | Original correct department among queued | Concise queued | Concise correct department among queued |
| ---: | ---: | ---: | ---: | ---: |
| 0.0 | 12 / 12 | 5 / 12 | 12 / 12 | 11 / 12 |
| 0.1 | 4 / 12 | 4 / 4 | 10 / 12 | 10 / 10 |
| 0.5 | 0 / 12 | — | 3 / 12 | 3 / 3 |
| 0.8 | 0 / 12 | — | 0 / 12 | — |
| 0.9 | 0 / 12 | — | 0 / 12 | — |

An empty queue has undefined queue accuracy, shown as a dash. The three queued tickets at threshold 0.5 in the concise run had correct departments; this does not prove that all other predictions were suitable. At threshold 0.1, T10 was queued with an urgency score of `1.0505` although its expected urgency is zero. The policy still assigned normal priority because its high-priority boundary is `1.5`. Department-only queue accuracy does not describe urgency-score errors.

These thresholds were replayed on the same teaching data, not validated for deployment. In particular, the shared `0.8` threshold produced zero coverage for both Laya runs. Choose measures and thresholds per application, question, and backend, then evaluate on held-out data. The official Jev service's confidence semantics and performance remain a separate live experiment.
