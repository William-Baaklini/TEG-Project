# python -m uvicorn app.backend.main:app --reload

from fastapi import FastAPI, UploadFile, File
from typing import List
import io

from app.backend.agents.manual_pipeline import run_pipeline
from app.backend.agents.planner_executer import run_planner_executor

app = FastAPI()

@app.post("/summarize")
async def summarize(file: UploadFile = File(...)):
    transcript_text = await file.read()
    decoded_text = transcript_text.decode("utf-8")

    # Dummy summary logic
    result = run_pipeline(decoded_text)

    return {
        "summary": result,
        "actions": action_items
    }