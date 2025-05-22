from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .agent import TutorAgent

app = FastAPI(title="Lumina Learn API")
agent = TutorAgent()


class Question(BaseModel):
    question: str


class Answer(BaseModel):
    answer: str


@app.get("/health", response_model=dict)
async def health() -> dict:
    """Health check endpoint."""
    return {"status": "ok"}


@app.post("/ask", response_model=Answer)
async def ask_question(question: Question) -> Answer:
    """Ask the TutorAgent a question."""
    try:
        answer_text = await agent.ask(question.question)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return Answer(answer=answer_text)


# For local testing: `uvicorn src.main:app --reload`
