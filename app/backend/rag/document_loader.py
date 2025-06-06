from langchain_community.document_loaders import TextLoader, PyPDFLoader
from pathlib import Path

def load_documents_from_directory(directory: str):
    all_docs = []

    for file_path in Path(directory).rglob("*"):
        if file_path.suffix == ".md" or file_path.suffix == ".txt":
            loader = TextLoader(str(file_path), encoding='utf-8')
        elif file_path.suffix == ".pdf":
            loader = PyPDFLoader(str(file_path))
        else:
            continue  # skip unsupported file types

        all_docs.extend(loader.load())

    return all_docs