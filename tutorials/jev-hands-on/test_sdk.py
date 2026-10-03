"""Test the real SDK with an in-memory HTTP transport, without network or model inference."""

import copy
import contextlib
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock
from common import route, workload
from run_hosted import build_questions
import run_hosted
from test_policy import fixture

try:
    import httpx2
    from typesafe_sdk import (RetryPolicy, TypeSafeClient, TypeSafeAuthenticationError,
                              TypeSafeAPIResponseValidationError)
except ImportError:
    httpx2 = None


@unittest.skipIf(httpx2 is None, "Install requirements-hosted.txt for SDK transport tests")
class SDKTests(unittest.TestCase):
    def client(self, handler):
        return TypeSafeClient(api_key="offline-test-key", model="jev-1.13.0",
                              transport=httpx2.MockTransport(handler),
                              retry=RetryPolicy(max_retries=0))

    def response(self):
        response = copy.deepcopy(fixture())
        response.update(model="jev-1.13.0", usage={"input_tokens": 100, "output_tokens": 40})
        response["answers"]["urgency"]["legend"] = {
            str(i): value for i, value in enumerate(workload()["questions"]["urgency"]["criteria"])
        }
        return response

    def test_request_encoding_and_response_work_with_application_policy(self):
        data = workload()
        def handler(request):
            self.assertEqual(request.method, "POST")
            self.assertEqual(str(request.url), "https://api.typesafe.ai/v1/systemone")
            body = json.loads(request.content)
            self.assertEqual(body["state"], data["tickets"][0]["text"])
            self.assertEqual(body["model"], "jev-1.13.0")
            self.assertEqual(body["questions"], data["questions"])
            return httpx2.Response(200, json=self.response())
        with self.client(handler) as client:
            response = client.system_one(state=data["tickets"][0]["text"], questions=build_questions(data))
        # SDK Python maps have integer Score keys; JSON export converts them to strings.
        self.assertEqual(set(response.answers["urgency"].probabilities), {0, 1, 2})
        exported = response.model_dump(mode="json")
        self.assertEqual(set(exported["answers"]["urgency"]["probabilities"]), {"0", "1", "2"})
        self.assertEqual(route(exported)["queue"], "billing")

    def test_http_401_is_an_authentication_error(self):
        with self.client(lambda request: httpx2.Response(401, json={"error": "Unauthorized"})) as client:
            with self.assertRaises(TypeSafeAuthenticationError):
                client.system_one(state="test", questions=build_questions(workload()))

    def test_malformed_success_payload_is_not_a_prediction(self):
        payload = self.response()
        payload["answers"]["refund_requested"]["noul"] = "yes"
        with self.client(lambda request: httpx2.Response(200, json=payload)) as client:
            with self.assertRaises(TypeSafeAPIResponseValidationError):
                client.system_one(state="test", questions=build_questions(workload()))

    def test_runner_records_a_failed_attempt_and_stops(self):
        client = self.client(lambda request: httpx2.Response(401, json={"error": "Unauthorized"}))
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "failed.json"
            with mock.patch.dict(os.environ, {"TYPESAFE_API_KEY": "offline-test-key"}), \
                 mock.patch.object(sys, "argv", ["run_hosted.py", "--limit", "2", "--output", str(target)]), \
                 mock.patch("typesafe_sdk.TypeSafeClient", return_value=client), \
                 contextlib.redirect_stdout(io.StringIO()):
                with self.assertRaises(SystemExit):
                    run_hosted.main()
            result = json.loads(target.read_text())
            self.assertFalse(result["completed"])
            self.assertEqual(result["requested_tickets"], 2)
            self.assertEqual(result["error_type"], "TypeSafeAuthenticationError")
            self.assertEqual(len(result["records"]), 1)
            self.assertIsNone(result["records"][0]["response"])
            self.assertEqual(result["summary"]["valid_outputs"], 0)
            self.assertEqual(result["summary"]["human_review"], 1)


if __name__ == "__main__":
    unittest.main()
