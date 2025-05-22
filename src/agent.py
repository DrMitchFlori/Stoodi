class TutorAgent:
    """Simple placeholder TutorAgent that returns canned responses."""

    def ask(self, question: str) -> str:
        """Return a placeholder answer for a given question."""
        if not question:
            raise ValueError("Question must not be empty")
        # In a real implementation, integrate with an LLM or RAG pipeline.
        return f"This is a placeholder answer to: '{question}'"
