import streamlit as st
from backend.api.Chains import get_chat_chain

@st.cache_resource
def load_chain():
    return get_chat_chain()



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
        chain = load_chain()
        res = chain.invoke({"input":user_input})
        st.success("Thinking Done\n")
        st.write(res)