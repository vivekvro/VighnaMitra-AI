import streamlit as st
import requests
import tempfile
atud_url = "https://vighnamitra-api.onrender.com//main/atud"
upload_url = "https://vighnamitra-api.onrender.com//main/upload"



def Uploadbotton(url,source_type,upload_file):
    if source_type in ["url","usertext"]:
        if st.button(f"upload {source_type}"):
                with st.spinner("Uploading.........."):
                    response = requests.post(
                        url=url,
                        json={"source_type":source_type,
                                    "upload_file":upload_file})
                    result = response.json()
                    st.success(result['status'])
    elif source_type in ["pdf","txt"]:
        if st.button("upload file"):
            with tempfile.NamedTemporaryFile(delete=False,suffix=".{source_type}") as tmp:
                tmp.write(upload_file.read())
                tmp.flush()
            upload_file = tmp.name
            with st.spinner("Uploading.........."):
                response = requests.post(
                    url=upload_url,
                    json={"source_type":source_type,
                                "upload_file":upload_file})
                result = response.json()
                st.success(result['status'])


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
        Uploadbotton(upload_url,source_type,upload_file)
    userquery = st.text_area("Enter Your Query: ")


elif source_type=="usertext":
    upload_file = st.text_area("Enter your topics")
    if upload_file:
        Uploadbotton(upload_url,source_type,upload_file)
    userquery = st.text_area("Enter Your Query: ")


# user url

elif source_type=="url":
    upload_file = st.text_input("Here Enter your Url, for example: https://example.com")
    if upload_file:
        Uploadbotton(upload_url,source_type,upload_file)
    userquery = st.text_area("Enter Your Query: ")

if st.button("Ask"):
    with st.spinner("Thinking.........."):
        response = requests.post(url=atud_url,
                                json={"userquery":userquery})
        result = response.json()
        st.success("Done.\n")
        st.write(result['response'])