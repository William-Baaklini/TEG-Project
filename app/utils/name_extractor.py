import re
from typing import List

def extract_speaker_names(transcript: str) -> List[str]:
    pattern = re.compile(r"\*\*\[\d{2}:\d{2}:\d{2}\]\s([^:]+):\*\*")
    matches = pattern.findall(transcript)
    # Remove duplicates and preserve order
    seen = set()
    unique_names = []
    for name in matches:
        if name not in seen:
            seen.add(name)
            unique_names.append(name)
    return unique_names
