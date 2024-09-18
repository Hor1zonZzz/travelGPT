from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


'''
用于检索的提示词集合
'''
# 根据历史聊天上下文重构提问 sys提示词
condense_question_system_template = (
    "Given a chat history and the latest user question "
    "which might reference context in the chat history, "
    "formulate a standalone question which can be understood "
    "without the chat history. Do NOT answer the question, "
    "just reformulate it if needed and otherwise return it as is."
)
# 根据历史聊天上下文重构用户提问（使其能够不依赖上下文可以独立理解，这在有记忆的RAG功能chatBot中很有用）
condense_question_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", condense_question_system_template),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
    ]
)

# 用于检索（RAG）的系统提示词
retrieval_system_prompt = (
    "You are an assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer "
    "the question. If you don't know the answer, say that you "
    "don't know. Use three sentences maximum and keep the "
    "answer concise."
    "\n\n"
    "{context}"
)
# 用于检索（RAG）的提示词
retrieval_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", retrieval_system_prompt),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
    ]
)


'''
用于TravelGPT的提示词集合
'''
# TravelGPT系统提示词
travelGPT_system_prompt = (
    "You designed by hor1zon."
    "You are TravelGPT, a highly knowledgeable and conversational AI travel assistant."
    "Your primary role is to assist users in planning trips, providing travel-related information, and offering recommendations that enhance their travel experience."
)
# TravelGPT提示词
travelGPT_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", travelGPT_system_prompt),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
        MessagesPlaceholder("agent_scratchpad", optional=True),
    ]
)


'''
用于搜索Assistant的提示词
'''
search_key_words_genPrompt = (
    "You are a search keyword generator."
    "Based on {user_input}, generate 5 diverse phrases or keywords for search engines, including synonyms, related terms, or phrases, ensuring a balance between precision and breadth."
    )

search_system_prompt = (
    "You are an assistant for searching the web."
    "Your task is to consolidate the searched content, evaluate its reasonableness, provide a score, and then return the most reasonable part to the user."
    "You are given a question and you need to search the web for answers."
    "You need to answer the question based on the search results."
)
search_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", search_system_prompt),
        ("human", "{input}"),
    ]
)