from typing_extensions import Literal

from .state import PhilosopherState
from .settings import TOTAL_MESSAGES_SUMMARY_TRIGGER


def should_summarize_conversation(state: PhilosopherState) -> Literal["summarize_conversation_node", "__end__"]:
    """
    Determines whether to summarize the conversation or end.
    
    Returns:
        "summarize_conversation_node": If message count exceeds threshold
        "__end__": If message count is below threshold
    """
    messages = state["messages"]
    if len(messages) > TOTAL_MESSAGES_SUMMARY_TRIGGER:
        return "summarize_conversation_node"
    return "__end__"