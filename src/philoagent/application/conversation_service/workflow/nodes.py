

from langchain_core.messages import RemoveMessage
from langchain_core.runnables import RunnableConfig
from typing import Literal


from langgraph.prebuilt import ToolNode
from .state import PhilosopherState, state_to_str
from langgraph.graph import END
from . import settings
from .chain import get_philosopher_response_chain, get_conversation_summary_chain
from .tools import tools


retriever_node = ToolNode(tools)



async def conversation_node(state:PhilosopherState,config:RunnableConfig):
    summary = state.get("summary","")
    conversation_chain = get_philosopher_response_chain()
    response = await conversation_chain.ainvoke(
        {
            "messages":state["messages"],
            "summary":summary,
            "philosopher_name": state.get("philosopher_name", ""),
            "philosopher_perspective": state.get("philosopher_perspective", ""),
            "philosopher_style": state.get("philosopher_style", ""),
        },
        config,
    )
    return {"messages":response}


async def summarize_conversation_node(state: PhilosopherState):
    summary = state.get("summary", "")
    summary_chain = get_conversation_summary_chain(summary)

    response = await summary_chain.ainvoke(
        {
            "messages": state["messages"],
            "philosopher_name": state["philosopher_name"],
            "summary": summary,
        }
    )

    delete_messages = [
        RemoveMessage(id=m.id)
        for m in state["messages"][: -settings.TOTAL_MESSAGES_AFTER_SUMMARY]
    ]
    return {"summary": response.content, "messages": delete_messages}



async def summarize_context_node(state: PhilosopherState,) -> Literal["summarize_conversation_node", "__end__"]:
    context_summary_chain = get_conversation_summary_chain()
    
    response = await context_summary_chain.ainvoke(
        {
           "context":state["messages"][-1].content,
        }
    )
    state["messages"][-1].content = response.content
    return {}

async def connector_node(state:PhilosopherState):
    return {}