from fastapi import FastAPI, UploadFile, File, Form,APIRouter, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from backend.api.Chains import get_llm, get_rag_chain, get_chat_chain
from backend.rag.Retrievers import get_retriever
from pydantic import BaseModel
import tempfile
import os
app = FastAPI()
from typing import Dict

router = APIRouter()




# ---- Models ----

class QueryRequest(BaseModel):
    userquery: str

class TextUpload(BaseModel):
    source_type: str
    upload_file: str

retriever_store = {}
chain_store = {}


chat_sessions = {}

model = get_llm()

# =====================================
# FILE UPLOAD
# =====================================

@app.post("/main/upload_file")
async def upload_file(
    source_type: str = Form(...),
    file: UploadFile = File(...)
):
    contents = await file.read()

    suffix = ".pdf" if source_type == "pdf" else ".txt"

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(contents)
        temp_path = tmp.name

    retriever = get_retriever(temp_path, source_type)

    retriever_store["current"] = retriever
    chain_store["current"] = get_rag_chain(retriever, model)

    os.remove(temp_path)

    return {"status": "File Uploaded"}


# =====================================
# TEXT / URL UPLOAD
# =====================================

@app.post("/main/upload_text")
def upload_text(data: TextUpload):

    retriever = get_retriever(
        data.upload_file,
        data.source_type
    )

    retriever_store["current"] = retriever
    chain_store["current"] = get_rag_chain(retriever, model)

    return {"status": "Text/URL Uploaded"}


# =====================================
# ASK QUESTION
# =====================================


@router.post("/main/atud")
def ask_question(UserData: QueryRequest):

    chain = chain_store.get("current")

    if chain is None:
        raise HTTPException(
            status_code=400,
            detail="No source uploaded yet."
        )

    response = chain.invoke(UserData.userquery)

    return {"response": response}
app.include_router(router)

# =====================================
# NORMAL CHAT
# =====================================
chat_sessions: Dict[str, object] = {}

class UserChat(BaseModel):
    message: str
    session_id: str

@app.post("/main/chat")
def return_chatresponse(user: UserChat):

    if user.session_id not in chat_sessions:
        chat_sessions[user.session_id] = get_chat_chain()

    chain = chat_sessions[user.session_id]

    try:
        response = chain.invoke({"input": user.message})

        # 🔹 Extract actual text safely
        if hasattr(response, "content"):  
            final_output = response.content
        elif isinstance(response, dict):
            final_output = response.get("text", "")
        else:
            final_output = str(response)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"response": final_output}