from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from models import AgentRequest, AgentResponse
from agent import run_agent

app = FastAPI(title="Autonomous AI Document Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Autonomous AI Document Agent is running."}


@app.post("/agent", response_model=AgentResponse)
def agent_endpoint(payload: AgentRequest):
    try:
        return run_agent(payload.request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent execution failed: {str(e)}")


@app.get("/download")
def download_file(path: str):
    return FileResponse(
        path=path,
        filename=path.split("/")[-1],
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )