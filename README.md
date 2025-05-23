# Lumina Learn

This repository contains an early prototype of **Lumina Learn**, an AI-powered study companion inspired by the [design document](docs/design.md).

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

## Frontend

The `frontend/` directory contains a React application built with Vite.

### Development server

Ensure Node.js (>=18) and npm are installed. Then run:

```bash
cd frontend
npm install
npm run dev
```

The app will be served at `http://localhost:3000`.

### Production build

To create an optimized build:

```bash
cd frontend
npm install
npm run build
```

The static files will be generated in `frontend/dist/`.

