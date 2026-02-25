import streamlit as st
import requests

BACKEND_URL = st.secrets.get("BACKEND_URL", "https://your-backend-url.com")

UPLOAD_FILE_URL = f"{BACKEND_URL}/main/upload_file"
UPLOAD_TEXT_URL = f"{BACKEND_URL}/main/upload_text"
ATUD_URL = f"{BACKEND_URL}/main/atud"


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