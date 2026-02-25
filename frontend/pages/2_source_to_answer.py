import streamlit as st
import requests

BACKEND_URL = st.secrets["BACKEND_URL"]

UPLOAD_FILE_URL = f"{BACKEND_URL}/main/upload_file"
UPLOAD_TEXT_URL = f"{BACKEND_URL}/main/upload_text"
ATUD_URL = f"{BACKEND_URL}/main/atud"


def upload_source(source_type, upload_file):
    try:
        with st.spinner("Uploading..."):

            # ---- FILE UPLOAD ----
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

            # ---- TEXT / URL UPLOAD ----
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


# ================= UI =================

st.title("V-Mitra AI")
st.markdown("### Document Intelligence • Source-to-Answer")

source_type = st.selectbox(
    "Select Input Type:",
    ['pdf', 'txt', 'usertext', 'url']
)

upload_file = None
userquery = None

if source_type in ["pdf", "txt"]:
    upload_file = st.file_uploader("Upload File", type=[source_type])

elif source_type == "usertext":
    upload_file = st.text_area("Enter Text")

elif source_type == "url":
    upload_file = st.text_input("Enter URL")

if upload_file:
    if st.button("Upload"):
        upload_source(source_type, upload_file)

userquery = st.text_area("Enter Your Query")

if st.button("Ask"):
    try:
        with st.spinner("Thinking..."):
            response = requests.post(
                ATUD_URL,
                json={"userquery": userquery}
            )

            if response.status_code == 200:
                result = response.json()
                st.success("Done.")
                st.write(result.get("response", "No response"))
            else:
                st.error(f"Error: {response.status_code}")
                st.write(response.text)

    except Exception as e:
        st.error(f"Request failed: {e}")