import uuid
from langchain_community.chat_message_histories import SQLChatMessageHistory

sql_url = "sqlite:///memory.db"
def generate_session_id():
    return str(uuid.uuid4())

def get_session_history(session_id):
    '''在数据库中获取会话历史'''
    return SQLChatMessageHistory(session_id, sql_url)