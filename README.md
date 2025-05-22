# Lumina Learn

This repository contains an early prototype of **Lumina Learn**, an AI-powered study companion inspired by the design document in the `Project` file.

## Running the API

1. Ensure Python 3.11+ is installed.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the server:
   ```bash
   uvicorn src.main:app --reload
   ```
   The API will be available at `http://localhost:8000`.

## Endpoints

- `GET /health` – Simple health check returning `{"status": "ok"}`.
- `POST /ask` – Ask the `TutorAgent` a question.

## Running Tests

Execute the unit tests with:

```bash
python -m unittest discover tests
```

## Package Version

You can check the installed version programmatically:

```python
from src import __version__
print(__version__)
```

