"""
Requirements:
    pip install -U streamlit streamlit-chatbox pinecone pinecone-plugins
"""
import streamlit as st
from streamlit_chatbox import ChatBox, Markdown
from pinecone import Pinecone
from pinecone_plugins.assistant.models.chat import Message
from pinecone_plugins.assistant.control.core.client.exceptions import NotFoundException

# Hardcoded API key
API_KEY = "pcsk_3Gij7S_F9ECnCAGNy59PpLjaW4EQuzbELnut28WMGkQkvgS5vV46Ys3SX36s2PUW55qKQs"

# Initialize Pinecone Assistant
pc = Pinecone(api_key=API_KEY)
try:
    assistant = pc.assistant.Assistant(assistant_name="yteru")
except NotFoundException:
    st.error(
        "Error: Assistant 'selling.com assistant' not found. "
        "Create it in the Pinecone console or use a valid assistant name."
    )
    st.stop()

# Streamlit page configuration
st.set_page_config(page_title="Selling.com Assistant Chat", layout="centered")
st.title("💬 Selling.com Assistant Chat")

# Initialize ChatBox session
chat_box = ChatBox(use_rich_markdown=False)
chat_box.use_chat_name("main_chat")
chat_box.init_session()

# Helper to extract text from history item
def extract_text(item):
    if isinstance(item, dict):
        return item.get("message") or item.get("text") or item.get("content") or str(item)
    return getattr(item, "message", str(item))

# Capture user input and interact
if user_input := st.chat_input("You:"):
    chat_box.user_say(user_input)
    # Build context and get response
    messages = [Message(content=extract_text(msg)) for msg in chat_box.history]
    resp = assistant.chat(messages=messages)
    assistant_msg = resp.get("message", {}).get("content", "")
    # Append assistant message
    chat_box.ai_say([Markdown(assistant_msg)])



# Clear chat history button
if st.button("Clear Chat"):
    chat_box.init_session(clear=True)
    try:
        st.rerun()
    except AttributeError:
        pass
