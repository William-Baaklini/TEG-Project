from langchain.agents import Tool
import json
from pathlib import Path
from app.utils.name_extractor import extract_speaker_names

PEOPLE_DB_PATH = Path("app/data/37signals_employees.json")

def load_people_db():
    with open(PEOPLE_DB_PATH, "r") as f:
        return json.load(f)

def assign_static_roles(transcript: str) -> str:
    names_in_meeting = extract_speaker_names(transcript)
    people_db = load_people_db()

    assigned = []
    for name in names_in_meeting:
        match = next((p for p in people_db if p["name"] == name), None)
        if match:
            assigned.append({
                "name": match["name"],
                "role": match["title"],  # or use a different role field
                "source": "static mapping"
            })
        else:
            assigned.append({
                "name": name,
                "role": "Unknown",
                "source": "not in database"
            })

    return json.dumps(assigned, indent=2)
