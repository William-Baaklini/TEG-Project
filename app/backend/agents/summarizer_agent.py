from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import AIMessage

from app.utils.toml_loader import load_toml_block
from app.utils.logger import logger

summarizer_template = load_toml_block("summarizer_agent")
summarizer_prompt = PromptTemplate(
    template=summarizer_template,
    input_variables=["input"]
)

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
output_parser = StrOutputParser()

summarizer_chain = summarizer_prompt | llm | output_parser

def summarizer_node(state):
    """
    Node that creates a comprehensive meeting summary.
    Uses 'transformed' data if available, otherwise falls back to last input message.
    """
    # Check if transformed data exists in state (from transformer node)
    if "transformed" in state and state["transformed"]:
        input_content = state["transformed"]
        logger.info('++Invoking Summarizier Agent with transformed str')
    elif "original_input" in state and state["original_input"]:
        input_content = state["original_input"]
        logger.info('++Invoking Summarizier Agent with original str')
    else:
        # Fall back to getting the last message content from input
        messages = state.get("input", [])
        if messages:
            last_message = messages[-1]
            if hasattr(last_message, "content"):
                input_content = last_message.content
            else:
                input_content = str(last_message)
        else:
            input_content = "Prompt the User That There's no Transcript Loaded"
            logger.warning('--Summarizer Agent Cannot Find Memory')
    
    # Process through the chain
    result = summarizer_chain.invoke({"input": input_content})
    
    return {
        'node': 'Summarizer',
        'summary': result,
        'input': [AIMessage(content=result)]
    }