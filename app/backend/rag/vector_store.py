from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

def build_vector_store(chunks, persist_directory="app/backend/rag/chroma_store"):
    embedding_fn = OpenAIEmbeddings(model="text-embedding-3-small")
    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_fn,
        persist_directory=persist_directory
    )
    return vectordb

def load_vector_store(persist_directory="app/backend/rag/chroma_store"):
    embedding_fn = OpenAIEmbeddings(model="text-embedding-3-small")
    return Chroma(
        embedding_function=embedding_fn,
        persist_directory=persist_directory
    )