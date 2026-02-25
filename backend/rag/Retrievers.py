from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

from dotenv import load_dotenv
from langchain_core.documents import Document
from typing import List
from backend.rag.LoadtoDocs import process_input


embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
def FaissRetreiver(docs: List[Document],embedding="sentence-transformers/all-MiniLM-L6-v2"):
    load_dotenv()
    Vec_Store = FAISS.from_documents(
        documents=docs,
        embedding=embeddings
    )
    return Vec_Store.as_retriever(search_kwargs={'k':10})


def get_retriever(usersource,source_type):
    docs = process_input(file_path=usersource,source_type=source_type)
    Retriever = FaissRetreiver(docs=docs)
    return Retriever



def get_retriever_context(docs):
    return "\n\n".join([doc.page_content for doc in docs])