from langchain.agents import Tool
from langchain_openai import ChatOpenAI
from app.utils.name_extractor import extract_speaker_names
from app.agents.static_role_tool import assign_static_roles
from app.backend.rag.retriever_wrapper import init_retriever

import json

from app.utils.prompt_loader import load_prompt

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
retriever = init_retriever()

def extract_actions_with_roles_and_rag(transcript: str) -> str:
    # Step 1: Retrieve relevant context
    context_docs = retriever.get_relevant_documents(transcript)
    context = "\n\n".join([doc.page_content for doc in context_docs])

    # Step 2: Get static role assignments
    role_data = json.loads(assign_static_roles(transcript))

    # Step 3: Format prompt
    role_context = "\n".join([f"{r['name']}: {r['role']}" for r in role_data])

    prompt = load_prompt("action_extraction", "template")

    return llm.predict(prompt)

# LangChain Tool
action_extractor_tool = Tool(
    name="extract_actions",
    func=extract_actions_with_roles_and_rag,
    description="Extracts action items from a transcript and assigns them based on roles and RAG knowledge"
)
