from app.backend.rag.document_loader import load_documents_from_directory
from app.backend.rag.chunking import chunk_documents
from app.backend.rag.vector_store import build_vector_store, load_vector_store
from app.utils.logger import logger
from pathlib import Path

# TODO try to improve the retrieval by using a more sophisticated retriever
def init_retriever(
    rag_path="app/data/rag_data", 
    rebuild=False, 
    search_kwargs=None,
    chunk_size=1000,
    chunk_overlap=200
):
    store_path = "app/backend/rag/chroma_store"
    
    # Default search parameters
    if search_kwargs is None:
        search_kwargs = {
            "k": 4,  # Number of documents to retrieve
            "fetch_k": 20,  # Number of documents to fetch before filtering
            "score_threshold": 0.5  # Minimum similarity score
        }

    if rebuild or not Path(store_path).exists():
        print("🔄 Rebuilding vector store...")
        docs = load_documents_from_directory(rag_path)
        chunks = chunk_documents(docs, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        vectordb = build_vector_store(chunks, store_path)
    else:
        vectordb = load_vector_store(store_path)

    return vectordb.as_retriever(search_kwargs=search_kwargs)


RAG_DATA_PATH = "app/data/rag_data"

logger.info("===== Initializing RAG Retriever")
retriever = init_retriever(rag_path=RAG_DATA_PATH, rebuild=False, search_kwargs={"k": 6,"fetch_k": 15, "score_threshold": 0.6}, chunk_size=1000, chunk_overlap=200)

__all__ = ["retriever"]