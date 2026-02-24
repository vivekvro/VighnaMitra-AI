from langchain_huggingface import ChatHuggingFace,HuggingFaceEndpoint
from dotenv import load_dotenv

def AutoChatModel(repo_id="openai/gpt-oss-20b",task="text-generation",max_new_tokens: int = 512,return_full_text:bool=False):
    load_dotenv()
    llm = HuggingFaceEndpoint(
        repo_id=repo_id,task=task,
        max_new_tokens=max_new_tokens,
        return_full_text=return_full_text
        )
    return ChatHuggingFace(llm=llm)


