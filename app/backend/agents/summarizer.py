from app.utils.prompt_loader import load_prompt
from app.backend.rag.retriever_wrapper import init_retriever
from langchain_openai import ChatOpenAI
from langchain.agents import Tool

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
retriever = init_retriever()

def generate_summary(transcript: str) -> str:
    context_docs = retriever.get_relevant_documents(transcript)
    context = "\n\n".join([doc.page_content for doc in context_docs])
    prompt_template = load_prompt("summarizer", "template")
    
    filled_prompt = prompt_template.format(context=context, transcript=transcript)
    return llm.predict(filled_prompt)

summarizer_tool = Tool(
    name="generate_summary",
    func=generate_summary,
    description="Generates a bullet-point summary of a transcript using RAG context"
)
