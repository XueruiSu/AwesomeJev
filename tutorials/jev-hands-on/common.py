"""Shared teaching workload and a conservative application policy. No inference here."""

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def workload():
    return json.loads((ROOT / "workload.json").read_text())


def number(value, low, high):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError("Expected a numeric value")
    if not math.isfinite(value) or not low <= value <= high:
        raise ValueError("Numeric value is outside its valid range")
    return value


def distribution(value, keys):
    if not isinstance(value, dict) or set(value) != set(keys):
        raise ValueError("Probability labels do not match the question")
    for p in value.values():
        number(p, 0, 1)
    if not math.isclose(sum(value.values()), 1, abs_tol=0.001):
        raise ValueError("Probabilities do not sum to one")
    return value


def validate(response):
    """Validate the three answers used by this application; extra metadata is allowed."""
    if not isinstance(response, dict) or not isinstance(response.get("answers"), dict):
        raise ValueError("Missing answer object")
    answers = response["answers"]
    for key, kind in [("department", "choice"), ("urgency", "score"), ("refund_requested", "noul")]:
        if not isinstance(answers.get(key), dict) or answers[key].get("type") != kind:
            raise ValueError("Missing answer or incorrect answer type: " + key)
    department = answers["department"]
    if department.get("choice") not in ("billing", "technical", "other"):
        raise ValueError("Unknown department")
    distribution(department.get("probabilities"), ("billing", "technical", "other"))
    number(department.get("confidence"), 0, 1)
    urgency = answers["urgency"]
    number(urgency.get("score"), 0, 2)
    number(urgency.get("confidence"), 0, 1)
    distribution(urgency.get("probabilities"), ("0", "1", "2"))
    number(answers["refund_requested"].get("noul"), 0, 1)
    return answers


def route(response, threshold=0.8):
    """Queue routing only. This policy never authorizes a refund or account change."""
    number(threshold, 0, 1)
    try:
        answers = validate(response)
    except (ValueError, TypeError, KeyError) as exc:
        return {"action": "human_review", "reason": "invalid_response", "detail": str(exc)}
    department, urgency = answers["department"], answers["urgency"]
    reasons = []
    if department["confidence"] < threshold:
        reasons.append("department_uncertain")
    if urgency["confidence"] < threshold:
        reasons.append("urgency_uncertain")
    refund_probability = answers["refund_requested"]["noul"]
    if max(refund_probability, 1 - refund_probability) < threshold:
        reasons.append("refund_intent_uncertain")
    if reasons:
        return {"action": "human_review", "reason": ",".join(reasons)}
    return {
        "action": "queue",
        "queue": department["choice"],
        "priority": "high" if urgency["score"] >= 1.5 else "normal",
        "refund_request_flag": refund_probability >= 0.5,
    }


def summarize(records):
    """Describe this tiny workload. Invalid outputs remain in the denominators."""
    valid, category_correct, refund_correct, urgency_errors, queued_correct = 0, 0, 0, [], 0
    queued = sum(r["policy"]["action"] == "queue" for r in records)
    for record in records:
        try:
            answers = validate(record["response"])
        except (ValueError, TypeError, KeyError):
            continue
        valid += 1
        expected = record["expected"]
        correct = answers["department"]["choice"] == expected["department"]
        category_correct += correct
        refund_correct += (answers["refund_requested"]["noul"] >= 0.5) == expected["refund_requested"]
        urgency_errors.append(abs(answers["urgency"]["score"] - expected["urgency"]))
        queued_correct += record["policy"]["action"] == "queue" and correct
    n = len(records)
    return {
        "tickets": n, "valid_outputs": valid, "department_correct": category_correct,
        "refund_intent_correct": refund_correct,
        "urgency_mae_on_valid": sum(urgency_errors) / valid if valid else None,
        "queued": queued, "human_review": n - queued,
        "queued_department_correct": queued_correct,
        "coverage": queued / n if n else 0,
        "note": "Synthetic teaching cases; not a representative benchmark or calibration study.",
    }
