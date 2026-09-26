from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

from .orchestrator import run_task


app = FastAPI(
    title="VeriForge AI",
    description="Multi-Agent AI Reasoning and Verification Engine"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"]
)


class TaskRequest(BaseModel):

    task: str


BASE_DIR = Path(__file__).resolve().parent.parent

FRONTEND_FILE = (
    BASE_DIR /
    "frontend" /
    "index.html"
)


@app.get("/")
def home():

    return FileResponse(
        FRONTEND_FILE
    )


@app.get("/health")
def health():

    return {
        "status": "healthy",
        "service": "VeriForge AI"
    }


@app.post("/run")
def run(request: TaskRequest):

    result = run_task(
        request.task
    )


    return {

        "task":
            result.get(
                "task",
                request.task
            ),

        "verification":
            result.get(
                "verification",
                {}
            ).get(
                "status",
                "unknown"
            ),

        "critic_risk":
            result.get(
                "critique",
                {}
            ).get(
                "risk",
                "unknown"
            ),

        "detected_risk":
            result.get(
                "risk",
                {}
            ).get(
                "risk",
                "unknown"
            ),

        "final_status":
            result.get(
                "final",
                {}
            ).get(
                "status",
                "unknown"
            ),

        "answer":
            result.get(
                "final",
                {}
            ).get(
                "answer"
            ),

        "attempts":
            result.get(
                "attempts",
                0
            )

    }