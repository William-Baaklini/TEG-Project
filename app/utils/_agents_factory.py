# app/agent_factory.py

from langchain.agents import AgentExecutor
from langchain_core.runnables import Runnable
from langchain_core.messages import AIMessage

def create_agent(agent_runnable, tools=None) -> Runnable:
    """
    Wraps a LangChain runnable agent with an optional toolset as an AgentExecutor.
    """
    if tools and len(tools) > 0:
        return AgentExecutor(agent=agent_runnable, tools=tools or [])
    else:
        return agent_runnable

def create_node(agent_executor: Runnable, name: str):
    """
    Wraps an AgentExecutor for LangGraph node compatibility.
    """
    def node(state):
        result = agent_executor.invoke(state)
        return {
            'node': name,
            'input': [AIMessage(content=result['output'])]
        }
    return node