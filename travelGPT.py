import os
import dotenv
import prompt
from operator import itemgetter
from interactDATA import get_session_history, generate_session_id
from langchain_core.messages import trim_messages
from langchain_core.runnables.history import RunnableWithMessageHistory, RunnablePassthrough
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()

model = ChatOpenAI(name="ChatAssistant", model="gpt-4o-2024-08-06")

# Load the prompt
prompt = prompt.travelGPT_prompt

# Create a session id for database
chat_session_id = generate_session_id()

# Create a config this config will be passed to during invoke
config = {
    "configurable": {
        "session_id": chat_session_id,
        }
}

# Trim the messages
trimmer = trim_messages(
    max_tokens=4096,
    token_counter=model,
    strategy="last",
)

# chain
chain = (
    RunnablePassthrough.assign(chat_history=itemgetter("chat_history") | trimmer) | prompt | model
)

# Create a runnable with history
runnable_with_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history",
)

# LOOP
while True:
    input_text = input("You: ")
    if input_text == "exit":
        break
    
    print("ChatGPT: ", end="")
    # 流式输出
    for chunk in runnable_with_history.stream(
        {"input": input_text},
        config = config
    ):
        print(chunk.content, flush=True, end="")
    print('\n')