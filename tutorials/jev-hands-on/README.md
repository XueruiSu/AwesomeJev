# Jev hands-on: from typed answers to a support queue

Learn the three decision types, make a hosted API request, and turn predictions into application behavior. The examples use twelve original, synthetic support tickets in [workload.json](workload.json). Expected labels follow an explicit urgency rubric; this small exercise is a teaching aid.

| Lesson | What you build | Where it runs |
| --- | --- | --- |
| [1. Typed decisions and the official API](01-typed-decisions.md) | A department label, urgency score, and refund-intent probability in one request | A lightweight Python client on your laptop; inference at TypeSafe |
| [2. Validation, routing, and evaluation](02-routing-and-evaluation.md) | A queue policy that sends malformed or uncertain answers to review | Standard Python; no model or API key needed for policy tests |
| [3. An independent open model on a remote GPU](03-remote-laya.md) | Run the same questions with a pinned Laya checkpoint | One free CUDA GPU on a remote Linux server |
| [Experiment notes](RESULTS.md) | Actual outputs, resource use, and lessons from this exercise | Read the evidence before drawing conclusions |

Jev receives **state** (the ticket) and **questions** (the decisions your program needs). Your code supplies the options and rubrics, then reads structured answers. Start with classification and routing rather than asking for a free-form conversation. The [official introduction](https://docs.typesafe.ai/introduction) and [primitive reference](https://docs.typesafe.ai/primitives/choice) describe the interface.

**Hosted Jev and Laya are separate models.** The official SDK calls TypeSafe's service. Laya is an independent, downloadable implementation in the wider decision-model ecosystem. Their shared question format makes a useful teaching comparison; their predictions, training, and confidence measures are not interchangeable.

## Start on a Mac without installing a model

From the repository root:

```bash
cd tutorials/jev-hands-on
python3 -m unittest test_policy -v
```

Five tests exercise queue routing, each uncertainty gate, malformed answers, threshold behavior, and evaluation denominators. They use explicitly hand-written fixtures; passing them does not show that a model understood a ticket.

For the official SDK, use Python 3.10 or later:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-hosted.txt
python -m unittest test_policy test_sdk -v
```

The extra four tests use the real SDK with an in-memory HTTP transport. They check request encoding, response conversion, authentication errors, malformed success payloads, and the runner's failure recording. They make no network calls. This environment contains no PyTorch or model weights.

If you have a TypeSafe API key, start with one real request:

```bash
python run_hosted.py --prompt-key --limit 1
```

Enter the key at the hidden prompt. Alternatively, use an already configured `TYPESAFE_API_KEY`. The key is not saved by this script. Requests use a paid or quota-limited service according to your account; starting with one ticket makes the request count explicit. Follow [lesson 1](01-typed-decisions.md) before running all twelve.

## Files and reproducibility

| File | Purpose |
| --- | --- |
| [workload.json](workload.json) | Shared questions, twelve tickets, and expected labels |
| [common.py](common.py) | Output validation, application routing, and small-workload metrics |
| [run_hosted.py](run_hosted.py) | Official API client, pinned model request, hidden key prompt, and failure recording |
| [run_laya.py](run_laya.py) | Remote-only GPU runner with revision and file-hash checks |
| [test_policy.py](test_policy.py), [test_sdk.py](test_sdk.py) | Offline checks; no inference evidence |

Run files, experiment snapshots, checkpoint manifests, environments, and download staging stay local and are ignored by Git. The runner contains the pinned revision and expected file hashes. [Experiment notes](RESULTS.md) retain the measured summary and selected predictions; generate your own run files to replay the evaluation. Keep new private tickets and credentials out of commits.

The GPU runner refuses macOS and requires exactly one selected CUDA device. Use [lesson 3](03-remote-laya.md) for installation and execution on a server; do not install the GPU requirements into your Mac environment.
