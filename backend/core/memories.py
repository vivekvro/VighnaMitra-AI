from langchain.memory import ConversationBufferMemory


def historyMemory():
    return ConversationBufferMemory(
    memory_key="history",
    return_messages=True
)