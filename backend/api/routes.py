from fastapi import FastAPI
from fastapi.responses import JSONResponse
from backend.api.Chains import get_llm, get_rag_chain,get_llm
from backend.rag.Retrievers import get_retriever
from pydantic import BaseModel

class QueryRequest(BaseModel):
    source_type:str
    upload_file: str
    userquery:str





app = FastAPI()

@app.post("/main/atud")
def return_pdfQnAresponse(UserData: QueryRequest):
    retriever = get_retriever(UserData.upload_file,UserData.source_type)
    model = get_llm()
    chain = get_rag_chain(retriever,model)
    chain_response = chain.invoke(UserData.userquery)
    return JSONResponse(content={"response":chain_response})