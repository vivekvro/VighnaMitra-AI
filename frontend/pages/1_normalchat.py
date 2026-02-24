import streamlit as st
import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from backend.api.Chains import get_chat_chain

@st.cache_resource
def load_chain():
    return get_chat_chain()
def get_user_chain():
    if "chat_chain" not in st.session_state:
        llm = get_chat_chain()
        st.session_state.chat_chain = get_chat_chain(llm)
    return st.session_state.chat_chain


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
        chain = get_user_chain()
        res = chain.invoke({"input":user_input})
        st.success("Thinking Done\n")
        st.write(res['text'])