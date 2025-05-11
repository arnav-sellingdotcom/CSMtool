import os
import streamlit as st
from pinecone import Pinecone
from pinecone_plugins.assistant.models.chat import Message
from pinecone_plugins.assistant.control.core.client.exceptions import NotFoundException

# Load API key (from GitHub Actions env or Streamlit secrets)
API_KEY = os.getenv("PINECONE_API_KEY") 
if not API_KEY:
    st.error("Missing Pinecone API key. Set PINECONE_API_KEY env var or in Streamlit secrets.")
    st.stop()

# Initialize Pinecone Assistant
pc = Pinecone(api_key=API_KEY)
try:
    assistant = pc.assistant.Assistant(assistant_name="yteru")
except NotFoundException:
    st.error(
        "Error: Assistant 'selling.com assistant' not found. "
        "Create it in the Pinecone console or use a valid name."
    )
    st.stop()

# Page config
st.set_page_config(page_title="Selling.com Assistant Chat", layout="centered")
st.title("💬 Selling.com Assistant Chat")

# Initialize chat history
if "history" not in st.session_state:
    st.session_state.history = []

# Display existing messages
for msg in st.session_state.history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Handle user input
if user_input := st.chat_input("You:"):
    # append user
    st.session_state.history.append({"role": "user", "content": user_input})
    # prepare Pinecone messages
    messages = [Message(content=m["content"]) for m in st.session_state.history]
    # get assistant reply
    resp = assistant.chat(messages=messages)
    text = resp.get("message", {}).get("content", "")
    st.session_state.history.append({"role": "assistant", "content": text})
    # rerun to show
    st.experimental_rerun()

# Clear chat button
if st.button("Clear Chat"):
    st.session_state.history = []
    st.experimental_rerun()
