import dotenv
import sqlite3
import travelGPT_prompt

from typing import Annotated
from typing_extensions import TypedDict

from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.messages import HumanMessage

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.checkpoint.memory import MemorySaver

from langchain_openai import ChatOpenAI

from toolCall import duckduckgo, get_weather

from drawGprah import draw_graph




dotenv.load_dotenv()

# create model
model = ChatOpenAI(model="gpt-4o-mini")
promptModel = ChatOpenAI(model="gpt-4o-mini")

# 将工具绑定到模型
search_tool = duckduckgo
tools_box = [search_tool]
model_with_tools = model.bind_tools(tools_box)

# 创建储存记忆和节点状态的数据库 (develop env use MemorySaver when production please use SqliteSaver)
# connect_to_sql = sqlite3.connect("memory.db", check_same_thread=False)
# memory_saver = SqliteSaver(connect_to_sql)
memory_saver = MemorySaver()

# 定义节点状态
class State(TypedDict):
    query: str
    key_words: list
    messages: Annotated[list, add_messages] # add_messages 定义了 messages 字段如何操作 由于ToolNode节点定义所以必须添加messages字段
 
 # 定义关键词输出的类（模型会按照此来结构化输出）
class Key_words_list(BaseModel):
    key_words_list: list[str]=Field(...,description="The list of key words")

# 定义节点中生成关键词的行为
def generate_key_words(state: State):
    prompt = travelGPT_prompt.search_key_words_genPrompt.format(user_input=state["query"])
    response = promptModel.with_structured_output(Key_words_list).invoke(prompt)
    return {
        "key_words": response.key_words_list,
        "messages": [state["query"]] # 这种直接添加到messages中的字符串会被自动转换为HumanMessage，根据State中的messages修饰会直接添加到messages中
        }

# 定义聊天模型在节点invoke
def chatbot(state: State):
    if type(state["messages"][-1]) == HumanMessage:
        Messages = [model_with_tools.invoke(state["key_words"][0])]
    else:
        Messages = [model_with_tools.invoke(state["messages"])]
    return {"messages": Messages}

tool_node = ToolNode(tools=tools_box) # ToolNode节点会自动将工具调用的输出返回到messages中

# define state 
graph_builder = StateGraph(State)

# add node
graph_builder.add_node("generate_key_words", generate_key_words)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", tool_node)

graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition,
    {"tools": "tools", "__end__": "__end__"}
)

graph_builder.add_edge(START, "generate_key_words")
graph_builder.add_edge("generate_key_words", "chatbot")
graph_builder.add_edge("tools", "chatbot")


# build graph
graph = graph_builder.compile(checkpointer=memory_saver)

# draw_graph(graph)


config = {"configurable": {"thread_id": "1"}}

for s in graph.stream({"query": "what is current weather in beijing"}, config=config):
    print(s)

sta = graph.get_state(config)
print(sta)
# while True:
#     user_input = input("User: ")
#     if user_input.lower() in ["quit", "exit", "q"]:
#         print("Goodbye!")
#         break
#     for event in graph.stream({"messages": ("query", user_input)}, config):
#         for value in event.values():
#             print("Assistant:", value["messages"][-1].content)
#             print("additional_kwargs:", value["messages"][-1].additional_kwargs)

