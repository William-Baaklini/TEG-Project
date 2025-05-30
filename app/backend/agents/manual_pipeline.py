from app.backend.agents.static_role_tool import assign_roles
from app.backend.agents.action_extractor import extract_actions
from app.backend.agents.summarizer import generate_summary

def run_pipeline(transcript: str) -> dict:
    # Step 1: Assign roles
    tagged_transcript = assign_roles(transcript)

    # Step 2: Extract action items
    actions = extract_actions(tagged_transcript)

    # Step 3: Generate summary
    summary = generate_summary(tagged_transcript)

    return {
        "summary": summary,
        "actions": actions
    }
