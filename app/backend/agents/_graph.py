from typing import Annotated, TypedDict, Optional

from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages
from langchain_core.runnables.graph import MermaidDrawMethod
from langchain_core.messages import HumanMessage, AIMessage
from langsmith import traceable

from app.utils.logger import logger

from app.backend.rag.retriever_wrapper import init_retriever

from app.backend.agents.transformer_agent import transformer_node
from app.backend.agents.action_items_agent import action_items_node
from app.backend.agents.summarizer_agent import summarizer_node
#todo add more nodes here

# Define the state
class AgentState(TypedDict):
    node: str
    roles: Optional[dict]
    original_input: Optional[str]
    transformed: Optional[str]
    actions: Optional[str]
    summary: Optional[str]
    input: Annotated[list, add_messages]

graph_builder = StateGraph(AgentState)

#todo add new nodes here
graph_builder.add_node("Transformer", transformer_node)
graph_builder.add_node("Action", action_items_node)
graph_builder.add_node("Summarizer", summarizer_node)

graph_builder.add_edge("Transformer", "Action")
graph_builder.add_edge("Action", "Summarizer")

graph_builder.set_entry_point("Transformer")
graph_builder.add_edge("Summarizer", END)
workflow = graph_builder.compile()

@traceable
def run_graph(transcript_text: str) -> dict:
    logger.info("Starting Multi-Agent Workflow...")

    input_message = HumanMessage(content=transcript_text)
    input = {
        "node": "User",
        "original_input": input_message,
        "input": [input_message]
    }
    last_msg = None
    final_state = None

    for event in workflow.stream(input, stream_mode="values"):
        node_name = event.get("node", "UNKOWN")
        messages = event.get("input", [])
        transformed = event.get("transformed", None)
        actions = event.get("actions", None)
        summary = event.get("summary", None)

        final_state = {
            "actions": actions,
            "summary": summary,
        }

        logger.info(f"===== Node executed {node_name}:")

        if transformed:
            logger.info(f"=== Transformed Data:\n{transformed}")
        if actions:
            logger.info(f"=== Actions:\n{actions}")
        if summary:
            logger.info(f"=== Summary:\n{summary}")
        if messages:
            last_msg = messages[-1]
            if hasattr(last_msg, "content"):
                logger.info(f"=== Message:\n{last_msg.content}")

    if final_state is None:
        logger.warning("Workflow finished but no output was received.")
        return {}
        
    logger.info("Workflow completed successfully.")
    return final_state

__all__ = ["run_graph"]