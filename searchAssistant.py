import os
import re
import json
import dotenv
import prompt
from interactDATA import get_session_history, generate_session_id
from toolCall import duckduckgo, get_weather
from langchain_community.document_loaders import WebBaseLoader
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

dotenv.load_dotenv()

searchGPT = ChatOpenAI(name="searchAssistant", model="gpt-4o-2024-08-06")

tools = [
    duckduckgo,
    get_weather
]

searchGPT_with_tools = searchGPT.bind_tools(tools, tool_choice="any")

# chain = prompt.search_prompt | searchGPT_with_tools

print(searchGPT_with_tools.invoke("北京市的天气怎么样?").tool_calls)

print(searchGPT_with_tools.invoke("北京的天气怎么样?"))

