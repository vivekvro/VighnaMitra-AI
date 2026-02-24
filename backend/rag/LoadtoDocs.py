from langchain_community.document_loaders import TextLoader,WebBaseLoader,PyMuPDFLoader,PyPDFLoader,DirectoryLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import Optional,List,Literal


#------------------------- Splitters ---------------------------------------------------#

def Splitter_docs(text,chunk_size=900,chunk_overlap=150,separators=["\n```","\nclass","\ndef",'\n\n',".\n",". ","\n"," ",""]):
    splitter = RecursiveCharacterTextSplitter(separators=separators,chunk_size=chunk_size,chunk_overlap=chunk_overlap)
    return splitter.split_documents(text)


def Splitter_text(docs,chunk_size=900,chunk_overlap=150,separators=["\n```","\nclass","\ndef",'\n\n',".\n","\n"]):
    splitter = RecursiveCharacterTextSplitter(separators=separators,chunk_size=chunk_size,chunk_overlap=chunk_overlap)
    return splitter.split_text(docs)


#------------------------- FileLoaders ---------------------------------------------------#


# pdf loader


def load_pdf(upload_file):
    loader = PyMuPDFLoader(upload_file)
    return loader.load()

# txt file loader


def load_txt(upload_file):
    loader = TextLoader(upload_file)
    return loader.load()

def load_url(urls):
    loader = WebBaseLoader(urls)
    return loader.load()



#---------------------- Processing ---------------------------------------#

def process_input(
        file_path:Optional[str]=None,
        source_type:Optional[Literal["pdf","txt","url","usertext"]]=None
        ) -> List[Document]:

    if source_type=="usertext":
        chunks = Splitter_text(file_path)
        return [Document(page_content=chunk,metadata={"source":"user_text"}) for chunk in chunks]

    elif source_type=="url":
        pageloader= WebBaseLoader(file_path)
        docs = pageloader.load()


    elif source_type=="pdf":
            docs = load_pdf(file_path)


    elif source_type=="txt":
            docs = load_txt(file_path)

    return Splitter_docs(docs)
