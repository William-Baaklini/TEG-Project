from pathlib import Path

def summarize_transcript(transcript_text: str) -> dict:
    # TODO: Replace with actual OpenAI call
    # For now, return dummy data
    summary = "This is a summary of the transcript."
    action_items = [
        {"task": "Prepare Q3 budget", "assigned_to": "Alice"},
        {"task": "Send meeting notes", "assigned_to": "Bob"},
    ]
    return {
        "summary": summary,
        "action_items": action_items
    }

from dotenv import load_dotenv
import os

load_dotenv()  # Automatically loads from .env

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
