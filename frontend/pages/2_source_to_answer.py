import streamlit as st
import requests
import tempfile

# Correct URLs (no double slash)
BASE_URL = "https://vighnamitra-api.onrender.com"
atud_url = f"{BASE_URL}/main/atud"
upload_url = f"{BASE_URL}/main/upload"


def Uploadbotton(source_type, upload_file):
    try:
        if source_type in ["url", "usertext"]:
            if st.button(f"Upload {source_type}"):
                with st.spinner("Uploading..."):
                    response = requests.post(
                        url=upload_url,
                        json={
                            "source_type": source_type,
                            "upload_file": upload_file
                        }
                    )

                    if response.status_code == 200:
                        result = response.json()
                        st.success(result.get("status", "Uploaded"))
                    else:
                        st.error(f"Error: {response.status_code}")
                        st.write(response.text)

        elif source_type in ["pdf", "txt"]:
            if st.button("Upload file"):
                with tempfile.NamedTemporaryFile(delete=False, suffix=f".{source_type}") as tmp:
                    tmp.write(upload_file.read())
                    tmp.flush()
                    temp_path = tmp.name

                with st.spinner("Uploading..."):
                    response = requests.post(
                        url=upload_url,
                        json={
                            "source_type": source_type,
                            "upload_file": temp_path
                        }
                    )

                    if response.status_code == 200:
                        result = response.json()
                        st.success(result.get("status", "Uploaded"))
                    else:
                        st.error(f"Error: {response.status_code}")
                        st.write(response.text)

    except Exception as e:
        st.error(f"Upload failed: {e}")


# ================= UI =================

st.title("V-Mitra AI")

st.markdown("""
### Document Intelligence • Source-to-Answer
---
Upload a source and ask your question.
---
""")

source_type = st.selectbox(
    "Select Your Doc input type:",
    ['pdf', 'usertext', 'txt', 'url']
)

# File inputs
if source_type in ["pdf", "txt"]:
    upload_file = st.file_uploader(
        f"Upload Your {source_type}",
        type=[source_type]
    )
    if upload_file is not None:
        Uploadbotton(source_type, upload_file)

    userquery = st.text_area("Enter Your Query:")

elif source_type == "usertext":
    upload_file = st.text_area("Enter your topics")
    if upload_file:
        Uploadbotton(source_type, upload_file)

    userquery = st.text_area("Enter Your Query:")

elif source_type == "url":
    upload_file = st.text_input(
        "Enter your URL (example: https://example.com)"
    )
    if upload_file:
        Uploadbotton(source_type, upload_file)

    userquery = st.text_area("Enter Your Query:")

# Ask section
if st.button("Ask"):
    try:
        with st.spinner("Thinking..."):
            response = requests.post(
                url=atud_url,
                json={"userquery": userquery}
            )

            if response.status_code == 200:
                result = response.json()
                st.success("Done.")
                st.write(result.get("response", "No response received."))
            else:
                st.error(f"Error: {response.status_code}")
                st.write(response.text)

    except Exception as e:
        st.error(f"Request failed: {e}")