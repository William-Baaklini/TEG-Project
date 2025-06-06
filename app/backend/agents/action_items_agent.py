
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import AIMessage

from app.utils.toml_loader import load_toml_block
from app.utils.logger import logger

action_items_template = load_toml_block("action_items_agent")
action_items_prompt = PromptTemplate(
    template=action_items_template,
    input_variables=["input"]
)

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
output_parser = StrOutputParser()

action_items_chain = action_items_prompt | llm | output_parser

def action_items_node(state):
    """
    Simple node that processes the input through the action items chain
    """
    if "transformed" in state and state["transformed"]:
        input_content = state["transformed"]
        logger.info('++Invoking Action Item Agent with transformed str')
    elif "original_input" in state and state["original_input"]:
        input_content = state["original_input"]
        logger.info('++Invoking Action Item Agent with original str')
    else:
        messages = state.get("messages", [])
        if messages:
            last_message = messages[-1]
            if hasattr(last_message, "content"):
                input_content = last_message.content
                logger.info('++Invoking Action Item Agent with transformed str')
            else:
                input_content = str(last_message)
        else:
            input_content = "Prompt the User That There's no Transcript Loaded"
            logger.warning('--Action Item Agent Cannot Find Memory')
    
    # Process through the chain
    result = action_items_chain.invoke({"input": input_content})
    
    return {
        'node': 'ActionItems',
        'actions': result,
        'input': [AIMessage(content=result)]
    }

__all__ = ["action_items_node"]