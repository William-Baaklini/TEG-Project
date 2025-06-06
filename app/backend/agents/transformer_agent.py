import json
import functools
from pathlib import Path

from langchain_core.tools import tool
from langchain_core.messages import AIMessage
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.agents import create_react_agent

from app.utils.name_extractor import extract_speaker_names
from app.utils.toml_loader import load_toml_block
from app.backend.agents.agents_factory import create_agent, create_node

def agent_node(state, agent, name):
    result = agent.invoke(state)
    return {
        'node': f"{name}",
        'input': [AIMessage(content=result['output'])]
    }

PEOPLE_DB_PATH = Path("app/data/37signals_employees.json")

def load_people_db():
    with open(PEOPLE_DB_PATH, "r") as f:
        return json.load(f)
    
@tool
def get_used_roles(transcript: str) -> str:
    """
    Extracts roles of people in the transcript using static rules and a people DB.
    Returns: JSON string of [{name, role}]
    """
    names_in_meeting = extract_speaker_names(transcript)
    people_db = load_people_db()

    assigned = []
    for name in names_in_meeting:
        match = next((p for p in people_db if p["name"] == name), None)
        assigned.append({
            "name": name,
            "role": f"{match['role']} L{match['level']}" if match else "Unknown"
        })
        
    return json.dumps(assigned, indent=2)

transformer_template = load_toml_block("transformer_agent")
transformer_prompt = PromptTemplate(
    template=transformer_template,
    input_variables=["input", "agent_scratchpad", "tools", "tool_names"]
)

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
tools = [get_used_roles]
react_agent = create_react_agent(llm, tools, transformer_prompt)
#TODO old to delete
# transformer_agent = AgentExecutor(agent=react_agent, tools=tools)
# transformer_node = functools.partial(agent_node, agent=transformer_agent, name="Transformer")

transformer_agent = create_agent(react_agent, tools=tools)
transformer_node = create_node(transformer_agent, name="Transformer")

__all__ = ["transfromer_agent", "transformer_node"]