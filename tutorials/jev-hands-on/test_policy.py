"""Offline policy tests. These hand-written fixtures are not model predictions."""

import copy
import unittest
from common import route, summarize


def fixture():
    return {"answers": {
        "department": {"type": "choice", "choice": "billing", "confidence": 0.95,
                       "probabilities": {"billing": 0.98, "technical": 0.01, "other": 0.01}},
        "urgency": {"type": "score", "score": 1.9, "confidence": 0.9,
                    "probabilities": {"0": 0, "1": 0.1, "2": 0.9}},
        "refund_requested": {"type": "noul", "noul": 0.99},
    }}


class PolicyTests(unittest.TestCase):
    def test_valid_ticket_routes_to_queue_without_payment_action(self):
        outcome = route(fixture())
        self.assertEqual(outcome, {"action": "queue", "queue": "billing", "priority": "high", "refund_request_flag": True})

    def test_every_uncertainty_dimension_can_escalate(self):
        for key, field in [("department", "confidence"), ("urgency", "confidence"), ("refund_requested", "noul")]:
            response = fixture()
            response["answers"][key][field] = 0.5
            self.assertEqual(route(response)["action"], "human_review")

    def test_malformed_and_missing_outputs_never_auto_route(self):
        missing = fixture(); del missing["answers"]["department"]
        unknown = fixture(); unknown["answers"]["department"]["choice"] = "payments"
        bad_sum = fixture(); bad_sum["answers"]["department"]["probabilities"]["billing"] = 0.5
        nan = fixture(); nan["answers"]["urgency"]["score"] = float("nan")
        bool_score = fixture(); bool_score["answers"]["urgency"]["score"] = True
        wrong_type = fixture(); wrong_type["answers"]["refund_requested"]["type"] = "boolean"
        for response in [None, {}, missing, unknown, bad_sum, nan, bool_score, wrong_type]:
            with self.subTest(response=response):
                self.assertEqual(route(response)["reason"], "invalid_response")

    def test_threshold_changes_coverage_not_the_model_response(self):
        response = fixture(); response["answers"]["department"]["confidence"] = 0.85
        before = copy.deepcopy(response)
        self.assertEqual(route(response, 0.8)["action"], "queue")
        self.assertEqual(route(response, 0.9)["action"], "human_review")
        self.assertEqual(before, response)

    def test_invalid_prediction_is_not_dropped_from_metrics(self):
        expected = {"department": "billing", "urgency": 2, "refund_requested": True}
        records = [{"response": r, "expected": expected, "policy": route(r)} for r in [fixture(), {}]]
        report = summarize(records)
        self.assertEqual(report["tickets"], 2)
        self.assertEqual(report["valid_outputs"], 1)
        self.assertEqual(report["department_correct"], 1)
        self.assertEqual(report["coverage"], 0.5)


if __name__ == "__main__":
    unittest.main()
