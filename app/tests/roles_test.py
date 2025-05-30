from pathlib import Path
import json

from app.utils.name_extractor import extract_speaker_names
from app.backend.agents.static_role_tool import assign_static_roles

# Load sample transcript
TRANSCRIPT_PATH = Path("app/data/37signals_transcript_technical.md")
transcript_text = TRANSCRIPT_PATH.read_text(encoding="utf-8")

# Step 1: Extract speaker names
names = extract_speaker_names(transcript_text)
print("🔍 Detected speaker names:")
print(names)

# Step 2: Assign roles using static DB
assigned_roles_json = assign_static_roles(transcript_text)
print("\n📌 Assigned Roles:")
print(assigned_roles_json)
