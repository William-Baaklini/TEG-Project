
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import AIMessage

from app.backend.rag.retriever_wrapper import retriever

from app.utils.toml_loader import load_toml_block
from app.utils.logger import logger

action_items_template = load_toml_block("action_items_agent")
action_items_prompt = PromptTemplate(
    template=action_items_template,
    input_variables=["input", "context"]
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

    context_parts = []
    if "roles" in state and state["roles"]:
        roles_query = (
            "This meeting involved the following team members and their roles:\n" +
            "\n".join(f"- {r['name']} is a {r['role']}" for r in state["roles"]) +
            "\nProvide any relevant project documentation or responsibilities based on these roles."
        )
        context_parts.append(roles_query)
        logger.info(f'Added roles context for {len(state["roles"])} team members')

        # Step 3: Get additional RAG context using roles as query context
        try:
            if retriever:
                docs = retriever.invoke(roles_query)
                if docs:
                    doc_context = "Additional context from knowledge base:\n" + "\n".join([doc.page_content[:500] + "..." if len(doc.page_content) > 500 else doc.page_content for doc in docs[:2]])
                    context_parts.append(doc_context)
                    logger.info(f'Added RAG context from {len(docs)} documents')
                else:
                    logger.info('No relevant documents found for roles-based query')
            else:
                logger.warning('RAG retriever not available')
        except Exception as e:
            pass
    
    # Combine all context
    final_context = "\n\n".join(context_parts) if context_parts else "No additional context available."
    
    # Process through the chain
    result = action_items_chain.invoke({"input": input_content, "context": final_context})
    
    return {
        'node': 'ActionItems',
        'actions': result,
        'input': [AIMessage(content=result)]
    }

__all__ = ["action_items_node"]