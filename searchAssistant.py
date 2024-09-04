import dotenv
import sqlite3

from typing import Annotated
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.sqlite import SqliteSaver

from langchain_openai import ChatOpenAI

from toolCall import duckduckgo, get_weather

from drawGprah import draw_graph




dotenv.load_dotenv()

# create model
model = ChatOpenAI(model="gpt-4o-2024-08-06")

# create tool
search_tool = duckduckgo
tools_box = [search_tool, get_weather]

model_with_tools = model.bind_tools(tools_box)

# create memory (develop env use MemorySaver when production please use SqliteSaver)
connect_to_sql = sqlite3.connect("memory.db", check_same_thread=False)
memory_saver = SqliteSaver(connect_to_sql)

class State(TypedDict):
    messages: Annotated[list, add_messages]

#define node
def chatbot(state: State):
    return {"messages": [model_with_tools.invoke(state["messages"])]}

tool_node = ToolNode(tools=tools_box)

# define state 
graph_builder = StateGraph(State)

# add node
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", tool_node)

graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition,
    {"tools": "tools", "__end__": "__end__"}
)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("tools", "chatbot")


# build graph
graph = graph_builder.compile(checkpointer=memory_saver)

# draw_graph(graph)


config = {"configurable": {"thread_id": "1"}}

while True:
    user_input = input("User: ")
    if user_input.lower() in ["quit", "exit", "q"]:
        print("Goodbye!")
        break
    for event in graph.stream({"messages": ("user", user_input)}, config):
        for value in event.values():
            print("Assistant:", value["messages"][-1].content)
            print("additional_kwargs:", value["messages"][-1].additional_kwargs)
