import streamlit as st
import requests
import tempfile
atud_url = "http://127.0.0.1:8000/main/atud"

# headings etc section
st.title("V-Mitra AI")

st.markdown("""
### Document Intelligence • Source-to-Answer
---
Transform your documents, URLs, or text into actionable insights.

Upload a source, ask your question, and receive precise, context-aware answers powered by Retrieval-Augmented Generation (RAG).

---
            """)


# select
source_type = st.selectbox("Select Your Doc input type: ",['pdf','usertext','txt','url'])

#============= pdf and txt file ========================== 

file_list=["pdf","txt"]
if source_type in file_list:
    upload_file = st.file_uploader(f"Upload Your {source_type}",type=[source_type])
    if upload_file is not None:
        userquery = st.text_area("Enter Your Query: ")
        with tempfile.NamedTemporaryFile(delete=False,suffix=".{source_type}") as tmp:
            tmp.write(upload_file.read())
            tmp.flush()
        upload_file = tmp.name







elif source_type=="usertext":
    upload_file = st.text_area("Here Enter your any Para or topic")
    userquery = st.text_area("Enter Your Query: ")


# user url

elif source_type=="url":
    upload_file = st.text_input("Here Enter your Url, for example: https://example.com")
    userquery = st.text_area("Enter Your Query: ")

if st.button("Ask"):
    with st.spinner("Thinking.........."):
        response = requests.post(url=atud_url,
                                json={"source_type":source_type,
                                    "upload_file":upload_file,
                                    "userquery":userquery})
        result = response.json()
        st.success("Done.\n")
        st.write(result['response'])