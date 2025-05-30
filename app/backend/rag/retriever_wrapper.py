from app.backend.rag.document_loader import load_markdown_documents
from app.backend.rag.chunking import chunk_documents
from app.backend.rag.vector_store import build_vector_store, load_vector_store
from pathlib import Path

def init_retriever(rag_path="app/rag_data", rebuild=False):
    store_path = "app/backend/rag/chroma_store"

    if rebuild or not Path(store_path).exists():
        print("🔄 Rebuilding vector store...")
        docs = load_markdown_documents(rag_path)
        chunks = chunk_documents(docs)
        vectordb = build_vector_store(chunks, store_path)
    else:
        vectordb = load_vector_store(store_path)

    return vectordb.as_retriever()
