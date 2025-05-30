from langchain_community.document_loaders import TextLoader
from pathlib import Path

def load_markdown_documents(directory: str):
    all_docs = []
    for file_path in Path(directory).rglob("*.md"):
        loader = TextLoader(str(file_path), encoding='utf-8')
        all_docs.extend(loader.load())
    return all_docs