


from langgraph.prebuilt import tools_condition
from langgraph.graph import START, END, StateGraph
from .state import PhilosopherState, state_to_str
from .nodes import conversation_node, summarize_conversation_node, summarize_context_node, retriever_node, connector_node
from .edges import should_summarize_conversation

def create_simple_workflow():
    graph_builder = StateGraph(PhilosopherState)

    # Add nodes
    graph_builder.add_node("conversation_node", conversation_node)
    graph_builder.add_node("retrieve_philosopher_context", retriever_node)
    graph_builder.add_node("summarize_conversation_node", summarize_conversation_node)
    graph_builder.add_node("summarize_context_node", summarize_context_node)
    graph_builder.add_node("connector_node", connector_node)

    # Define edges
    graph_builder.add_edge(START, "conversation_node")

    # tools_condition returns "tools" or "__end__"
    graph_builder.add_conditional_edges(
        "conversation_node",
        tools_condition,
        {
            "tools": "retrieve_philosopher_context",
            "__end__": "connector_node"
        }
    )

    graph_builder.add_edge("retrieve_philosopher_context", "summarize_context_node")
    graph_builder.add_edge("summarize_context_node", "conversation_node")

    # should_summarize_conversation returns "summarize_conversation_node" or "__end__"
    graph_builder.add_conditional_edges(
        "connector_node",
        should_summarize_conversation,
        {
            "summarize_conversation_node": "summarize_conversation_node",
            "__end__": END
        }
    )
    graph_builder.add_edge("summarize_conversation_node", END)

    return graph_builder