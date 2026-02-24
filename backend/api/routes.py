from fastapi import FastAPI
from fastapi.responses import JSONResponse
from backend.api.Chains import get_llm, get_rag_chain,get_llm,get_chat_chain
from backend.rag.Retrievers import get_retriever
from pydantic import BaseModel

class QueryRequest(BaseModel):
    userquery:str
class File_upload(BaseModel):
    source_type:str
    upload_file: str

class UserChat(BaseModel):
    message:str


app = FastAPI()

retriever_store = {}
model = get_llm()   # load once


@app.post("/main/upload")
def upload_file(data: File_upload):

    retriever = get_retriever(data.upload_file, data.source_type)

    retriever_store["current"] = retriever

    return {"status": "*Uploaded*"}

@app.post("/main/atud")
def return_pdfQnAresponse(UserData: QueryRequest):

    retriever = retriever_store.get("current")

    if retriever is None:
        return {"error": "No document processed yet"}

    chain = get_rag_chain(retriever, model)
    chain_response = chain.invoke(UserData.userquery)

    return {"response": chain_response}


@app.post("/main/chat")
async def return_chatresponse(user: UserChat):
        chain = get_chat_chain()
        response = chain.invoke({"input":user.message})
        return JSONResponse(content={"response":response['text']})
