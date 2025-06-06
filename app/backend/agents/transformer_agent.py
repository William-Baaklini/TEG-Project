import re
import json
from pathlib import Path

from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.messages import AIMessage

from app.utils.name_extractor import extract_speaker_names
from app.utils.toml_loader import load_toml_block

PEOPLE_DB_PATH = Path("app/data/37signals_employees.json")

def load_people_db():
    with open(PEOPLE_DB_PATH, "r") as f:
        return json.load(f)
    
def clean_json_output(output: str) -> str:
    """
    Clean the LLM output by removing markdown code blocks and extra whitespace.
    """
    # Remove ```json and ``` markers
    cleaned = re.sub(r'```json\s*', '', output)
    cleaned = re.sub(r'\s*```', '', cleaned)

    # Strip leading/trailing whitespace
    cleaned = cleaned.strip()

    return cleaned
    
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
transformer_agent = AgentExecutor(
    agent=react_agent, 
    tools=tools, 
    max_iterations=5,          # Max iterations before stopping
    max_execution_time=60,     # Max time in seconds
    early_stopping_method="generate",  # Stop when agent thinks it's done
    handle_parsing_errors=True,        # Handle malformed outputs gracefully
    return_intermediate_steps=True,    # Get step-by-step execution info
    verbose=True) #Speaks trail of thoughts

def transformer_node(state):
    result = transformer_agent.invoke(state)

    result = clean_json_output(result['output'])

    try:
        # Attempt to parse the result as JSON
        parsed_result = json.loads(result)
        
        # Extract roles from the transcript if it's a list of messages
        if isinstance(parsed_result, list) and all(isinstance(item, dict) for item in parsed_result):
            # Use a set to track unique name-role combinations
            seen_combinations = set()
            roles = []
            
            for item in parsed_result:
                if 'name' in item and 'role' in item:
                    # Create a tuple of name and role for uniqueness checking
                    combination = (item['name'], item['role'])
                    if combination not in seen_combinations:
                        seen_combinations.add(combination)
                        roles.append({
                            'name': item['name'],
                            'role': item['role']
                        })
            
            # Add roles to the return dictionary
            return {
                'node': "Transformer",
                'transformed': result,
                'input': [AIMessage(content=result)],
                'roles': roles
            }
    except json.JSONDecodeError:
        # If JSON parsing fails, return the original result without roles
        pass

    return {
        'node': "Transformer",
        'transformed': result,
        'input': [AIMessage(content=result)]
    }

__all__ = ["transformer_agent", "transformer_node"]