# 1. Typed decisions with the official Jev API

[Back to the tutorial](README.md) · [Next: routing and evaluation](02-routing-and-evaluation.md)

Our application needs three answers for each incoming support ticket:

| Type | Question | Application field | Interpretation |
| --- | --- | --- | --- |
| Choice | Which team handles this? | `department` | One of `billing`, `technical`, or `other`, with a probability for each option |
| Score | How urgent is the stated situation? | `urgency` | An expected score on ordered levels 0, 1, 2; it may be fractional |
| Noul | Does the customer explicitly ask for money back? | `refund_requested` | A number from 0 to 1 representing the yes probability |

These types are documented in the [Choice](https://docs.typesafe.ai/primitives/choice), [Score](https://docs.typesafe.ai/primitives/score), and [Noul](https://docs.typesafe.ai/primitives/noul) references. **Noul is the primitive's name.** A value of `0.5` is uncertainty, not an ordinary Python boolean.

The ticket is state, not a request to let the model perform an action. Refund intent is just a flag; a separate application would need its own authorization and payment workflow.

## Describe one decision per question

Read [workload.json](workload.json) before calling the service. It contains three independently answerable questions. Department options explain their boundaries; urgency levels describe stated impact rather than topic; refund intent excludes complaints that do not ask for money back.

Compare T09 (a bill explanation, explicitly no refund) with T06 (return the unused month's payment). This distinction is useful when writing criteria: the word “bill” alone should not determine the refund flag.

An `other` department gives the model somewhere to put press requests and public-report queries. It is not an uncertainty label: the model can be confident that an unrelated ticket belongs there, or uncertain between ordinary departments.

## Install and make one call

Use the laptop setup in the [tutorial README](README.md#start-on-a-mac-without-installing-a-model). The official [quick start](https://docs.typesafe.ai/introduction/quickstart) explains how to obtain an API key from the TypeSafe console. We pin `typesafe-sdk==0.7.2` and request `jev-1.13.0` rather than a moving `jev-latest` alias.

```bash
python run_hosted.py --prompt-key --limit 1
```

This sends T01 once, requests all three answers, prints the queue/review decision, and writes `runs/hosted.json`. Model inference happens at TypeSafe; your Mac runs the small client. The script disables automatic retries so the exercise does not silently make extra attempts. A timeout can still leave the server-side outcome uncertain.

The essential SDK call is:

```python
from common import workload
from run_hosted import build_questions
from typesafe_sdk import RetryPolicy, TypeSafeClient

data = workload()
with TypeSafeClient(model="jev-1.13.0", timeout=30,
                    retry=RetryPolicy(max_retries=0)) as client:
    response = client.system_one(
        state=data["tickets"][0]["text"],
        questions=build_questions(data),
    )
print(response.answers["department"].choice)
print(response.answers["urgency"].score)
print(response.answers["refund_requested"].noul)
```

Use an already configured `TYPESAFE_API_KEY` for this short snippet. The full runner also offers the hidden key prompt.

## Read the result before using it

Choice and Score provide both `probabilities` and `confidence`. Official Noul answers provide `noul` without a separate confidence field. Confidence summarizes the distribution; it is not measured accuracy on your application. The [official confidence documentation](https://docs.typesafe.ai/confidence) explains the formulas and their interpretation.

SDK Score maps use integer level keys in Python. Exporting with `response.model_dump(mode="json")` gives string keys such as `"0"`, matching a JSON response. Our policy deliberately operates on this exported representation. An offline transport test checks this conversion against the installed SDK.

After inspecting the first response and your account access, run the entire teaching corpus:

```bash
python run_hosted.py --prompt-key --limit 12 --output runs/hosted-all.json
```

Inspect `requested_model`, the response's `model`, `completed`, `error_type`, and the summary. A requested identifier alone does not prove which model answered. Do not compare a failed or partial run with a completed evaluation without showing the difference.

## Troubleshoot a failed call

| Symptom | What to check |
| --- | --- |
| Missing-key message before any call | Supply `TYPESAFE_API_KEY` or use `--prompt-key`; a GitHub token is not a TypeSafe key |
| `TypeSafeAuthenticationError` | Check the TypeSafe credential and account access |
| `TypeSafePermissionDeniedError` / `TypeSafeNotFoundError` | Confirm the account can access the requested model; explicitly record any changed identifier |
| `TypeSafeRateLimitError` | Check the service's response/account quota before making another attempt |
| `TypeSafeAPIConnectionError` / `TypeSafeAPITimeoutError` | Check DNS, HTTPS access, and the network proxy; do not disable TLS verification |
| `TypeSafeAPIResponseValidationError` | Inspect the SDK version and response shape; do not treat the failed parse as a prediction |

On an API failure during the loop, the runner records `response: null`, an error class, and a review outcome, then stops with a nonzero exit. It preserves prior successful records. Raw files stay ignored. The current [experiment notes](RESULTS.md) distinguish offline SDK validation from any live hosted evaluation.
