import unittest

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


if __name__ == "__main__":
    unittest.main()
