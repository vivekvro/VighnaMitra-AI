from langchain_core.messages import SystemMessage

def ChatAssistantMessage(systemContent:str):
    return [SystemMessage(content="You are Helpful Assistant.Help user with their questions, and Answer in very polite way. do not miss behave, or do not give answers to those questions about which You do not have information, just reply 'Sorry i do not have information related to this question'")]

print(ChatAssistantMessage())