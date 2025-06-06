from pathlib import Path

from app.backend.agents._graph import run_graph

transcript_path = Path("app/data/37signals_transcript_technical.md")
transcript_text = transcript_path.read_text(encoding="utf-8")

run_graph(transcript_text=transcript_text)