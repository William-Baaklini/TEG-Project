# python -m app.tests.rag_test "what are the titles for programmers?"
from app.backend.rag.retriever_wrapper import init_retriever
import sys

if __name__ == "__main__":
    # Initialize the retriever with rebuild=True to ensure fresh vector store
    retriever = init_retriever(rag_path="app/rag_data/37signals_md")
    
    # Get query from command line or user input
    query = sys.argv[1] if len(sys.argv) > 1 else input("Enter your search query: ")
    
    # Get relevant documents using invoke
    docs = retriever.invoke(query)
    
    # Print results
    print(f"\n🔍 Query: {query}\n")
    print("📄 Relevant Documents:")
    if not docs:
        print("No documents found!")
    for i, doc in enumerate(docs, 1):
        print(f"\n--- Document {i} ---")
        print(doc.page_content)
        print(f"Source: {doc.metadata.get('source', 'Unknown')}")