# python -m uvicorn app.backend.main:app --reload

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from typing import List
import io
import json

from app.backend.agents._graph import run_graph

app = FastAPI()

@app.post("/run")
async def summarize(file: UploadFile = File(...)):
    transcript_text = await file.read()
    decoded_text = transcript_text.decode("utf-8")

    result = run_graph(transcript_text=decoded_text)

    print(result)

    summary = result.get("summary", "No Summary Was Found")
    actions_raw = result.get("actions", {})

    # If actions is a JSON string, parse it
    try:
        actions = json.loads(actions_raw) if isinstance(actions_raw, str) else actions_raw
    except json.JSONDecodeError:
        actions = {"error": "Failed to parse actions"}

    return JSONResponse(content={
        "summary": summary,
        "actions": actions
    })