import streamlit as st
import requests

url = "http://127.0.0.1:8000/main/chat"

st.title("🧠 VighnaMitra AI")

st.markdown("""
## 💬 Chat with VighnaMitra

Welcome! You can have intelligent conversations with your AI companion here.

### What you can do:
- Ask questions about any topic  
- Learn concepts step-by-step  
- Brainstorm ideas  
- Get explanations and guidance  

### 📝 Note:
- If a response isn’t helpful, please provide feedback to help improve VighnaMitra.
- Feel free to ask anything — curiosity is encouraged!

---
Start your conversation below 👇
""")

user_input = st.text_area("Enter Your message: ")
if st.button("Send"):
    with st.spinner("Thinking.........."):
        response = requests.post(
            url=url,
            json={"message":user_input}
                )
        result = response.json()
        st.success("Thinking Done\n")
        st.write(result['response'])