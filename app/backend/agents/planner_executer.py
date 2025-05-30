from langchain.agents import create_openai_functions_agent, AgentExecutor, tool
from langchain.agents.agent_toolkits import Tool
from langchain.chains import LLMChain
from langchain.schema import SystemMessage
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.agents import RunnableAgent

from langchain_openai import ChatOpenAI

# Import tools
from app.backend.agents.summarizer import summarizer_tool
from app.backend.agents.action_extractor import action_extractor_tool
from app.backend.agents.static_role_tool import role_tool

# Initialize LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Define Planner Prompt
prompt = ChatPromptTemplate.from_messages([
    SystemMessage(content=(
        "You are a project assistant AI that can summarize meeting transcripts, "
        "assign roles, and extract action items. Based on the user's request, choose the right tools."
    )),
    MessagesPlaceholder(variable_name="chat_history"),
    MessagesPlaceholder(variable_name="input")
])

# Build the agent
agent = create_openai_functions_agent(
    llm=llm,
    tools=[summarizer_tool, action_extractor_tool, role_tool],
    prompt=prompt,
)

# Wrap with executor
executor = AgentExecutor(agent=agent, tools=[summarizer_tool, action_extractor_tool, role_tool], verbose=True)

# 🔹 ENTRY POINT FUNCTION
def run_planner_executor(user_query: str, transcript: str):
    return executor.invoke({
        "chat_history": [],
        "input": f"{user_query}\n\nTranscript:\n{transcript}"
    })
