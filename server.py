import os
import streamlit as st
from pinecone import Pinecone
from pinecone_plugins.assistant.models.chat import Message
from pinecone_plugins.assistant.control.core.client.exceptions import NotFoundException

# Load API key from env var or Streamlit secrets
API_KEY = os.getenv("PINECONE_API_KEY") or st.secrets.get("pinecone", {}).get("api_key")
if not API_KEY:
    st.error("Missing Pinecone API key. Set PINECONE_API_KEY env var or add it to Streamlit secrets.")
    st.stop()

# Initialize Pinecone Assistant
pc = Pinecone(api_key=API_KEY)
try:
    assistant = pc.assistant.Assistant(assistant_name="yteru")
except NotFoundException:
    st.error("Error: Assistant 'yteru' not found. Create it in the Pinecone console or use a valid name.")
    st.stop()

# Page config
st.set_page_config(page_title="Selling.com Assistant Chat", layout="centered")
st.title("💬 Selling.com Assistant Chat")

# Initialize chat history
if "history" not in st.session_state:
    st.session_state.history = []  # list of {"role": "user"|"assistant", "content": str}

# Display existing conversation
for msg in st.session_state.history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Handle user input
if user_input := st.chat_input("You:"):
    # 1) Append user message
    st.session_state.history.append({"role": "user", "content": user_input})

    # 2) Build context
    messages = [Message(content=m["content"]) for m in st.session_state.history]

    # 3) Show spinner while waiting
    with st.spinner("🤔 Assistant is thinking..."):
        resp = assistant.chat(messages=messages)

    # 4) Extract assistant reply and append
    assistant_text = resp.get("message", {}).get("content", "")
    st.session_state.history.append({"role": "assistant", "content": assistant_text})

    # 5) Rerun so the updated history is rendered at the top
    try:
        st.rerun()
    except AttributeError:
        pass

# Clear chat history
if st.button("Clear Chat"):
    st.session_state.history = []
    try:
        st.rerun()
    except AttributeError:
        pass
