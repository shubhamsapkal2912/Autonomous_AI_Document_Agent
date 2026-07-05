# Fluid AI Assignment - Autonomous AI Document Agent

## Features
- FastAPI backend
- POST /agent endpoint
- Accepts natural language requests
- Creates its own task plan
- Makes assumptions when details are missing
- Generates a polished .docx business document
- Includes request validation and fallback behavior

## Run
```bash
source venv/bin/activate
uvicorn app:app --reload
```

## Test
Open:
- http://127.0.0.1:8000/docs

Example payload:
```json
{
  "request": "Create a project proposal for implementing an AI chatbot for a retail company."
}
```