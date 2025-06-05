# python -m uvicorn app.backend.main:app --reload

from fastapi import FastAPI, UploadFile, File
from typing import List
import io

from app.backend.agents._graph import run_graph

app = FastAPI()

@app.post("/run")
async def summarize(file: UploadFile = File(...)):
    transcript_text = await file.read()
    decoded_text = transcript_text.decode("utf-8")

    result = run_graph(decoded_text)

    return result