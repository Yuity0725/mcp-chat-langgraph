import operator
from typing_extensions import TypedDict
from typing import Any, Callable, Dict, Iterable, List, Optional, TypedDict, Annotated

from langchain_core.messages import AnyMessage

from langgraph.prebuilt import ToolNode
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver


class GraphState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]


def create_graph(state: GraphState, tools, model_chain):
    def should_continue(state: state):
        messages = state["messages"]
        last_message = messages[-1]
        if last_message.tool_calls:
            return "tools"
        return END


    def call_model(state: state):
        messages = state["messages"]
        response = model_chain.invoke(messages)
        return {"messages": [response]}


    tool_node = ToolNode(tools)
    
    workflow = StateGraph(state)
    workflow.add_node("agent", call_model)
    workflow.add_node("tools", tool_node)

    workflow.add_edge(START, "agent")
    workflow.add_conditional_edges("agent", should_continue, ["tools", END])
    workflow.add_edge("tools", "agent")
    memory = MemorySaver()
    app = workflow.compile(checkpointer=memory)
    
    return app