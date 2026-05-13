"""Chains for the philosopher agent workflow."""
from pathlib import Path
import sys

root_path = Path(__file__).resolve().parents[4]  # goes to src
sys.path.insert(0, str(root_path))

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import Runnable
from langchain_core.messages import BaseMessage
from langchain_groq import ChatGroq

from philoagent.domain.prompts import PHILOSOPHER_CHARACTER_CARD
from philoagent.config import settings
from .tools import tools

from typing import Any, Dict
import os
from dotenv import load_dotenv
load_dotenv()

def get_chat_model(temeperature:float=0.7, model_name:str|None=None)->ChatGroq:
    """Helper function to create a chat model with the specified temperature."""
    if model_name is None:
        model_name = settings.GROQ_LLM_MODEL
    return ChatGroq(
        api_key=settings.GROQ_API_KEY,
        model_name=model_name,
        temperature=temeperature
    )
    # from langchain_core.chat_models import ChatOpenAI
    # return ChatOpenAI(model="gpt-3.5-turbo", temperature=temeperature)

def get_philosopher_response_chain() -> Runnable:
    """
    Creates and returns a chain for generating philosopher responses.
    
    Returns:
        Runnable: A chain that takes messages and summary as input and returns a response.
    """
    model = get_chat_model()
    model = model.bind_tools(tools)
    system_message = PHILOSOPHER_CHARACTER_CARD
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_message.prompt),
            MessagesPlaceholder(variable_name="messages"),
        ],
        template_format='jinja2',
    )
    return prompt|model




def get_conversation_summary_chain(summary: str = "") -> Runnable:
    """
    Creates and returns a chain for summarizing conversations.
    
    Args:
        summary (str): The existing summary to build upon.
    
    Returns:
        Runnable: A chain that takes messages, philosopher info, and current summary as input
                 and returns an updated summary.
    """
    # TODO: Implement the actual summarization chain
    # This should use an LLM to generate concise summaries of the conversation
    
    from langchain_core.runnables import RunnableLambda
    
    async def generate_summary(state: Dict[str, Any]) -> BaseMessage:
        # Placeholder implementation
        # Replace with actual LLM chain
        from langchain_core.messages import AIMessage
        return AIMessage(content="Summary of the conversation so far...")
    
    return RunnableLambda(generate_summary)
