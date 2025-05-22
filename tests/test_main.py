import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from src.main import app


client = TestClient(app)


class APITestCase(unittest.TestCase):
    def test_health(self):
        response = client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

    def test_ask(self):
        response = client.post("/ask", json={"question": "What is the capital of France?"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("answer", data)
        self.assertIn("France", data["answer"])

    def test_empty_question(self):
        response = client.post("/ask", json={"question": ""})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"detail": "Question must not be empty"})

    def test_invalid_json(self):
        response = client.post(
            "/ask",
            data="{",
            headers={"Content-Type": "application/json"},
        )
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json(), {"detail": "Malformed JSON"})

    def test_unexpected_error(self):
        with patch("src.main.agent.ask", side_effect=RuntimeError("boom")):
            response = client.post("/ask", json={"question": "Hello"})
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json(), {"detail": "Internal Server Error"})


if __name__ == "__main__":
    unittest.main()
