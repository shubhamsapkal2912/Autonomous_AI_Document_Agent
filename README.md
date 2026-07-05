# Autonomous AI Document Agent

An AI-powered document generation app that turns plain-English business requests into structured documents through a FastAPI backend, a lightweight web UI, and a local Ollama model pipeline. The project is now deployed live with Docker and Nginx, and runs using the **Ollama Llama 3.3 3B** model for document planning and response generation.

<div align="center">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img alt="FastAPI" src="https://img.shields.io/badge/FastAPI-API-009688?style=for-the-badge&logo=fastapi&logoColor=white" />
  <img alt="Ollama" src="https://img.shields.io/badge/Ollama-Llama%203.3%203B-111827?style=for-the-badge" />
  <img alt="Docker" src="https://img.shields.io/badge/Docker-Containerized-2496ED?style=for-the-badge&logo=docker&logoColor=white" />
  <img alt="Nginx" src="https://img.shields.io/badge/Nginx-Production%20Hosting-009639?style=for-the-badge&logo=nginx&logoColor=white" />
</div>

## Live Demo

- Production URL: [shubhamsapkal.space](https://shubhamsapkal.space/)
- API docs (local FastAPI): `http://127.0.0.1:8000/docs`

## Overview

This project accepts a natural-language request, classifies the most suitable document type, builds an execution plan, and generates a polished business document. The backend includes validation, fallback behavior, and support for multiple business-oriented formats such as project proposals, meeting minutes, business reports, SOPs, product specs, and technical designs.

## Features

- Natural-language request input from a browser-based interface.
- FastAPI backend with a POST `/agent` endpoint.
- Local LLM integration using Ollama and the **Llama 3.3 3B** model.
- Automatic document type selection and structured planning.
- Fallback plan generation when model output is malformed or unavailable.
- Word document generation for business workflows.
- Clean frontend for testing prompts and downloading generated files.
- Container-friendly deployment with Docker and Nginx.

## Supported Document Types

| Type | Purpose |
|------|---------|
| `projectproposal` | Proposal for business or technical initiatives |
| `meetingminutes` | Structured meeting summary with actions and decisions |
| `businessreport` | General business analysis and summary document |
| `sop` | Standard operating procedure draft |
| `productspec` | Product requirement or feature specification |
| `technicaldesign` | Technical architecture or implementation design |

## Architecture

<div align="center">
  <pre>
  User Browser
      │
      ▼
  Static Frontend (HTML/CSS/JS)
      │
      ▼
  FastAPI Backend (/agent)
      │
      ├── Request validation (Pydantic)
      ├── Prompting + plan normalization
      ├── Ollama API call
      │       ▼
      │   Llama 3.3 3B
      │
      ▼
  Document Generator
      │
      ▼
  Downloadable .docx Output
  </pre>
</div>

## Flow Diagram

<div align="center">
  <pre>
  Request entered in UI
          │
          ▼
  API receives business prompt
          │
          ▼
  Model returns JSON plan
          │
      ┌───┴───────────────┐
      │                   │
      ▼                   ▼
  Valid JSON         Invalid / failed
      │                   │
      ▼                   ▼
  Normalize plan      Use fallback plan
      │                   │
      └───────┬───────────┘
              ▼
      Build document sections
              ▼
         Generate .docx
              ▼
         Return download link
  </pre>
</div>

## Project Structure

```text
.
├── app.py                # FastAPI application entry point
├── agent.py              # LLM orchestration, fallback logic, section builder
├── doc_generator.py      # Word document generation logic
├── models.py             # Request and response schemas
├── prompts.py            # System prompt definitions
├── index.html            # Frontend interface
├── README.md             # Project documentation
└── requirements.txt      # Python dependencies (if added separately)
```

## How It Works

1. The user enters a business request in the web UI.
2. The frontend sends the request to the FastAPI `/agent` endpoint.
3. The backend validates the payload using Pydantic models.
4. The agent sends a structured instruction to Ollama.
5. The LLM returns a JSON document plan.
6. The backend normalizes the plan and applies fallback logic if needed.
7. The document generator creates a `.docx` file.
8. The UI displays metadata and provides a download link.

## Local Setup

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd <your-project-folder>
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start Ollama

Make sure Ollama is installed and the Llama 3.3 3B model is available locally:

```bash
ollama pull llama3.3:3b
ollama serve
```

### 5. Configure environment variables

Create a `.env` file:

```env
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.3:3b
```

### 6. Run the FastAPI server

```bash
uvicorn app:app --reload
```

### 7. Open the app

- Frontend: open `index.html` in the browser, or serve it with Nginx
- API docs: `http://127.0.0.1:8000/docs`

## Docker Deployment

The app can be deployed with Docker for consistent packaging and Nginx for serving the frontend or reverse proxying backend traffic.

### Example deployment stack

- **Frontend hosting:** Nginx
- **Backend service:** FastAPI running in a container
- **Model runtime:** Ollama with `llama3.3:3b`
- **Public access:** [shubhamsapkal.space](https://shubhamsapkal.space/)

<div align="center">
  <pre>
         Internet
            │
            ▼
     shubhamsapkal.space
            │
            ▼
          Nginx
        ┌────┴────┐
        ▼         ▼
   Frontend     FastAPI
                    │
                    ▼
                 Ollama
             (llama3.3:3b)
  </pre>
</div>

### Example Docker commands

```bash
docker build -t autonomous-doc-agent .
docker run -p 8000:8000 autonomous-doc-agent
```

## Example Request

```json
{
  "request": "Create a project proposal for implementing an AI chatbot for a retail company to improve customer support."
}
```

## Example Output

The response includes:

- Document status
- Generated title
- Document type
- Execution plan
- Assumptions
- Download path for the generated Word file
- Fallback status

## Tech Stack

- Python
- FastAPI
- Pydantic
- HTML, CSS, JavaScript
- Ollama
- Llama 3.3 3B
- Docker
- Nginx
- python-docx or equivalent Word generation utilities

## Improvements You Can Add

- Authentication for user access.
- Persistent document history.
- Better prompt templates for each document type.
- Multi-model switching support.
- Queueing for long-running document jobs.
- Richer frontend styling and upload support.
- PDF export alongside DOCX generation.

MIT License

Copyright (c) 2026 Shubham


