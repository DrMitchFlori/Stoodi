from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from .agent import TutorAgent

app = FastAPI(title="Lumina Learn API")
agent = TutorAgent()


@app.exception_handler(HTTPException)
async def handle_http_exception(request: Request, exc: HTTPException) -> JSONResponse:
    """Return JSON responses for HTTP errors."""
    status = exc.status_code
    detail = exc.detail
    if status == 400 and detail == "There was an error parsing the body":
        status = 422
        detail = "Malformed JSON"
    return JSONResponse(status_code=status, content={"detail": detail})


@app.exception_handler(RequestValidationError)
async def handle_validation_error(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Simplify validation errors to a consistent JSON structure."""
    errors = exc.errors()
    is_json_error = (
        len(errors) == 1 and errors[0].get("type") == "value_error.jsondecode"
    )
    if is_json_error:
        return JSONResponse(status_code=422, content={"detail": "Malformed JSON"})
    return JSONResponse(
        status_code=422,
        content={"detail": "Validation failed", "errors": errors},
    )


@app.exception_handler(Exception)
async def handle_general_exception(request: Request, exc: Exception) -> JSONResponse:
    """Catch-all handler for unexpected errors."""
    return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})


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
        answer_text = await agent.ask(question.question.strip())
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return Answer(answer=answer_text)


# For local testing: `uvicorn src.main:app --reload`
