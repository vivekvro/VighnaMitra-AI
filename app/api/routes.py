from fastapi import FastAPI
from app.api.Chains import get_llm
from app.rag.LoadtoDocs import process_input

from app.api.Chains import get_retriever,get_rag_chain,get_llm


app = FastAPI()

@app.get("/main/{source_type}/{upload_pdf}/{userquery}")
def return_pdfQnAresponse(upload_file:str,source_type:str,userquery:str):
    retriever = get_retriever(upload_file,source_type)
    model = get_llm()
    chain = get_rag_chain(retriever,model)
    return chain.invoke(userquery)


