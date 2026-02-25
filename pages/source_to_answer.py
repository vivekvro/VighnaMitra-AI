import streamlit as st
import requests
import os
from dotenv import load_dotenv
load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL")

UPLOAD_FILE_URL = f"{BACKEND_URL}/main/upload_file"
UPLOAD_TEXT_URL = f"{BACKEND_URL}/main/upload_text"




def upload_source(source_type, upload_file):
    try:
        with st.spinner("Uploading..."):

            if source_type in ["pdf", "txt"]:
                files = {
                    "file": (upload_file.name, upload_file, upload_file.type)
                }
                data = {"source_type": source_type}

                response = requests.post(
                    UPLOAD_FILE_URL,
                    files=files,
                    data=data
                )

            else:
                response = requests.post(
                    UPLOAD_TEXT_URL,
                    json={
                        "source_type": source_type,
                        "upload_file": upload_file
                    }
                )

            if response.status_code == 200:
                st.success("Uploaded successfully.")
            else:
                st.error(f"Error: {response.status_code}")
                st.write(response.text)

    except Exception as e:
        st.error(f"Upload failed: {e}")



st.title("Source to answer")
st.markdown("""
#### this page is for Ansking questionf from Documents that user Uploads:
---""")







source_type = st.selectbox("Select Source Type:",['pdf','txt','url','usertext'])
if source_type in ["pdf",'txt']:
    upload_file = st.file_uploader(label=f"Upload your {source_type}",type=['pdf','txt'])
    if st.button("Upload now"):
        upload_source(source_type=source_type,upload_file=upload_file)
elif source_type=="url":
    upload_file = st.text_input(label="Enter Source URL")
    if st.button("Upload now"):
        upload_source(source_type=source_type,upload_file=upload_file)
elif source_type=="usertext":
    upload_file = st.text_area("Enter Text Source")
    if st.button("Upload now"):
        upload_source(source_type=source_type,upload_file=upload_file)

userquery = st.text_area("Enter Question")

if st.button("Ask"):

    if not userquery.strip():
        st.warning("Please enter a question")
        st.stop()

    with st.spinner("Thinking..."):

        try:
            res = requests.post(
                "http://127.0.0.1:8000/main/atud",
                json={"userquery": userquery}
            )

            data = res.json()

            if res.status_code == 200 and "response" in data:
                st.success("Response:")
                st.write(data["response"])

            elif "detail" in data:
                st.error(data["detail"])

            elif "error" in data:
                st.error(data["error"])

            else:
                st.error("Unexpected server response")

        except Exception as e:
            st.error(f"Connection Error: {e}")