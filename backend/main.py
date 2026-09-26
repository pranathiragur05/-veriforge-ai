from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from pathlib import Path

from .orchestrator import run_task


app = FastAPI(
    title="VeriForge AI",
    description="Multi-Agent AI Reasoning and Verification Engine"
)


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"]
)


# Request model
class TaskRequest(BaseModel):
    task: str


# Frontend path
BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_FILE = BASE_DIR / "frontend" / "index.html"


# Home page
@app.get("/")
def home():
    return FileResponse(FRONTEND_FILE)


# Run AI verification
@app.post("/run")
def run(request: TaskRequest):

    result = run_task(request.task)

    return {
        "task": result["task"],
        "verification": result["verification"]["status"],
        "critic_risk": result["critique"]["risk"],
        "detected_risk": result["risk"]["risk"],
        "final_status": result["final"]["status"],
        "answer": result["final"].get("answer"),
        "attempts": result["attempts"]
    }