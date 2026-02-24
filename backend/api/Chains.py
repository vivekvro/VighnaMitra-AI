from langchain_core.runnables import RunnableLambda,RunnableParallel,RunnableBranch,RunnableWithMessageHistory,RunnablePassthrough
from backend.rag.PromptsAndParsers import UserInputClassificationPrompt,InputClassifierParser as UserInputClassifierParser
from backend.rag.PromptsAndParsers import QuestionsFromDocumentPrompt, StrParser,ChatNormalPrompt
from backend.rag.Chatmodels import AutoChatModel
from backend.rag.LoadtoDocs import process_input
from backend.rag.Retrievers import FaissRetreiver,get_retriever_context,get_retriever
from backend.core.memories import historyMemory
from langchain.chains import LLMChain
import tempfile



def get_llm(model_repo_id = "openai/gpt-oss-20b"):
    return AutoChatModel(model_repo_id)

def get_userinput_classifier_chain(llm):
    return UserInputClassificationPrompt | llm | UserInputClassifierParser





def get_retriever_context_chain(usersource,source_type):
    retriever = get_retriever(usersource,source_type)
    return (
        {"context":retriever | RunnableLambda(get_retriever_context),
        "userinput":RunnablePassthrough()
        })


def get_rag_chain(Retriever,model):
    return (
        {"context":Retriever | RunnableLambda(get_retriever_context),
        "userinput":RunnablePassthrough()
        }
        | QuestionsFromDocumentPrompt
        | model
        | StrParser
    )

def get_chat_chain():
    return LLMChain(llm=AutoChatModel(),prompt=ChatNormalPrompt,memory=historyMemory())
