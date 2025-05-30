import toml
from pathlib import Path

PROMPT_DIR = Path("app/prompts")

def load_prompt(category: str, key: str = "template") -> str:
    path = PROMPT_DIR / f"{category}.toml"
    data = toml.load(path)
    return data.get(key) or data.get(category, {}).get(key)
