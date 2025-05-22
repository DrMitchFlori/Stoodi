import asyncio
import unittest

from src.main import app, health, ask_question, Question


class APITestCase(unittest.IsolatedAsyncioTestCase):
    async def test_health(self):
        response = await health()
        self.assertEqual(response, {"status": "ok"})

    async def test_ask(self):
        question = Question(question="What is the capital of France?")
        answer = await ask_question(question)
        self.assertIn("France", answer.answer)

    async def test_empty_question(self):
        with self.assertRaises(Exception):
            question = Question(question="")
            await ask_question(question)


if __name__ == "__main__":
    unittest.main()
