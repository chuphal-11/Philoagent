import langgraph
from langgraph.graph import MessagesState


class PhilosopherState(MessagesState):
    """State class for the LangGraph workflow. It keeps track of the information necessary to maintain a coherent
    conversation between the Philosopher and the user.

    Attributes:
        philosopher_context (str): The historical and philosophical context of the philosopher.
        philosopher_name (str): The name of the philosopher.
        philosopher_perspective (str): The perspective of the philosopher about AI.
        philosopher_style (str): The style of the philosopher.
        summary (str): A summary of the conversation. This is used to reduce the token usage of the model.
    """
    philosopher_context: str
    philosopher_name: str
    philosopher_perspective: str
    philosopher_style: str
    summary: str



def state_to_str(state: PhilosopherState) -> str:
    """Converts the state of the workflow to a string. This is used to provide the model with the necessary
    information to maintain a coherent conversation.

    Args:
        state (PhiloagentState): The state of the workflow.

    Returns:
        str: A string representation of the state.
    """
    if "summary" in state and bool(state["summary"]):
        conversation = state["summary"]
    elif "messages" in state and bool(state["messages"]):
        conversation= state["messages"]
    else:
        conversation=""
    return f"""
    PhilosopherState(
        philosopher_name={state["philosopher_name"]},
        philosopher_context={state["philosopher_context"]},
        philosopher_perspective={state["philosopher_perspective"]},
        philosopher_style={state["philosopher_style"]},
        conversation={conversation}
    )
    """
