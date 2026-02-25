import streamlit as st
import requests
import uuid

BACKEND_URL = st.secrets.get("BACKEND_URL", "https://your-backend-url.com")

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

st.title("🧠 VighnaMitra AI")

user_input = st.text_area("Enter your message:")

if st.button("Send") and user_input.strip():

    with st.spinner("Thinking..."):

        response = requests.post(
            f"{BACKEND_URL}/main/chat",
            json={
                "message": user_input,
                "session_id": st.session_state.session_id
            }
        )

        if response.status_code == 200:
            result = response.json()
            st.success("Done")
            st.write(result["response"])
        else:
            st.error(f"Error {response.status_code}")
            st.write(response.text)