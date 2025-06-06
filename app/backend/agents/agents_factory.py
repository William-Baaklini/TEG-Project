# app/agent_factory.py

from langchain.agents import AgentExecutor
from langchain_core.messages import AIMessage

def create_agent(agent_runnable, tools=None) -> AgentExecutor:
    """
    Wraps a LangChain runnable agent with an optional toolset as an AgentExecutor.
    """
    return AgentExecutor(agent=agent_runnable, tools=tools or [])


def create_node(agent_executor: AgentExecutor, name: str):
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