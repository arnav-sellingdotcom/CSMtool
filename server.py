import os
import streamlit as st
from pinecone import Pinecone
from pinecone_plugins.assistant.models.chat import Message
from pinecone_plugins.assistant.control.core.client.exceptions import NotFoundException

# Load API key from environment variable
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
        "Error: Assistant 'yteru' not found. "
        "Create it in the Pinecone console or use a valid assistant name."
    )
    st.stop()

# Streamlit page configuration
st.set_page_config(page_title="Selling.com Assistant Chat", layout="centered")
st.title("💬 Selling.com Assistant Chat")

# Initialize chat history
if "history" not in st.session_state:
    st.session_state.history = []  # list of {"role": "user"|"assistant", "content": str}

# Display existing messages
for msg in st.session_state.history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Handle user input
if user_input := st.chat_input("You:"):
    # Append user message
    st.session_state.history.append({"role": "user", "content": user_input})

    # Build context and get assistant reply
    messages = [Message(content=m["content"]) for m in st.session_state.history]
    resp = assistant.chat(messages=messages)
    assistant_text = resp.get("message", {}).get("content", "")

    # Append assistant response
    st.session_state.history.append({"role": "assistant", "content": assistant_text})

    # Rerun so Streamlit picks up the new messages
    st.experimental_rerun()

# Clear chat history button
if st.button("Clear Chat"):
    st.session_state.history = []
    st.experimental_rerun()
