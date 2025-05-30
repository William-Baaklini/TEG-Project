from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from typing import List
import io

app = FastAPI()

@app.post("/summarize")
async def summarize(file: UploadFile = File(...)):
    transcript_text = await file.read()
    decoded_text = transcript_text.decode("utf-8")

    # Dummy summary logic
    summary = "Demo summary."
    action_items = [
        {"task": "Prepare Q3 budget", "assigned_to": "Alice"},
        {"task": "Send meeting notes", "assigned_to": "Bob"},
    ]

    return {
        "summary": summary,
        "action_items": action_items
    }
