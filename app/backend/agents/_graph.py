from typing import Annotated, TypedDict

from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages
from langchain_core.runnables.graph import MermaidDrawMethod
from langchain_core.messages import HumanMessage, AIMessage
from langsmith import traceable

from app.utils.logger import logger

from app.backend.agents.transformer_agent import transformer_node
#todo add more nodes here

def log_node_execution(name: str, state: dict):
    logger.info(f"Node '{name}' executed with state keys: {list(state.keys())}")

# Define the state
class AgentState(TypedDict):
    node: str
    input: Annotated[list, add_messages]

graph_builder = StateGraph(AgentState)

#todo add new nodes here
graph_builder.add_node("transformer", transformer_node)
# graph_builder.on_node("transformer", log_node_execution)

graph_builder.set_entry_point("transformer")
graph_builder.add_edge("transformer", END)
workflow = graph_builder.compile()

@traceable
def run_graph(transcript_text: str) -> str:
    logger.info("Starting Multi-Agent Workflow...")

    input_message = HumanMessage(content=transcript_text)
    input = {
        "node": "User",
        "input": [input_message]
    }
    last_msg = None

    for event in workflow.stream(input, stream_mode="values"):
        node_name = event.get("node", "UNKOWN")
        messages = event.get("input", [])

        logger.info(f"Node executed: {node_name}")

        if messages:
            last_msg = messages[-1]
            if hasattr(last_msg, "content"):
                logger.info(f"Message from node {node_name}:\n{last_msg.content}")
            else:
                logger.debug(f"Message from node {node_name} has no 'content'.")

    if last_msg is None:
        logger.warning("Workflow finished, but no response was produced.")
        return ""
        
    if not hasattr(last_msg, "content"):
        logger.warning("Workflow finished, but response has no content.")
        return ""
        
    logger.info("Workflow completed successfully.")
    return last_msg.content