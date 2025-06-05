import tomllib
from pathlib import Path

PROMPT_FILE = Path("app/backend/prompts/prompts.toml")

def load_toml_block(prompt_name: str, key: str = "template", prompt_file: Path = PROMPT_FILE) -> str:
    with open(prompt_file, "rb") as f:  # tomllib requires binary mode
        data = tomllib.load(f)
    block = data.get(prompt_name)
    if block is None:
        raise KeyError(f"No prompt named '{prompt_name}' found.")
    
    value = block.get(key)
    if value is None:
        raise KeyError(f"Key '{key}' not found in prompt '{prompt_name}'.")
    
    return value