from langchain.agents import Tool
import json
from pathlib import Path
from app.utils.name_extractor import extract_speaker_names

PEOPLE_DB_PATH = Path("app/data/37signals_employees.json")

def load_people_db():
    with open(PEOPLE_DB_PATH, "r") as f:
        return json.load(f)

def assign_static_roles(transcript: str) -> str:
    """
    Assign roles to speakers based on static rules.
    Returns JSON string with role assignments.
    """
    names_in_meeting = extract_speaker_names(transcript)
    people_db = load_people_db()

    assigned = []
    for name in names_in_meeting:
        match = next((p for p in people_db if p["name"] == name), None)
        if match:
            assigned.append({
                "name": match["name"],
                "role": match["role"] + " L" + str(match["level"])
            })
        else:
            assigned.append({
                "name": name,
                "role": "Unknown",
            })

    return json.dumps(assigned, indent=2)

# Create the tool
role_tool = Tool(
    func=assign_static_roles,
    name="assign_roles",
    description="Assigns roles to people in a transcript based on a static database entries"
)
