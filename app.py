import streamlit as st

from src.config import SYSTEM_PROMPT
from src.knowledge_base import load_and_embed_knowledge
from src.retriever import run_llm
from src.search import serpapi_tool
from src.state import init_chat_state, get_current_chat, new_chat, switch_chat
from src.ui import render_custom_style, display_chat

# Initialize Streamlit page
st.set_page_config(page_title="Egypt Tour Guide Chatbot", layout="wide")
render_custom_style()

# Initialize chat state
init_chat_state()

# Sidebar UI for chat sessions
with st.sidebar:
    st.header("Chats")
    for sid, messages in st.session_state.chat_sessions.items():
        user_msg = next((m["content"] for m in messages if m["role"] == "user"), "")
        label = user_msg[:30] + "..." if user_msg else "(New Chat)"
        if st.button(label, key=sid):
            switch_chat(sid)
    if st.button("➕ New Chat"):
        new_chat()
        st.experimental_rerun()

# Display existing chat messages
display_chat()

# User input
query = st.chat_input("Ask me anything about Egypt...")

if query:
    chat = get_current_chat()
    # Append user message
    chat.append({"role": "user", "content": query})
    # Display immediately
    with st.chat_message("user"):
        st.markdown(f'<div class="user-msg">{query}</div>', unsafe_allow_html=True)

    # Typing indicator placeholder
    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.markdown('<div class="typing-bubble">Assistant is typing...</div>', unsafe_allow_html=True)

    # Build messages for LLM call
    messages = chat.copy()

    # Get answer from LLM
    answer = run_llm(messages)

    # If answer is short or uncertain, fallback to SerpAPI
    if "I'm not sure" in answer or len(answer.strip()) < 50:
        from src.search import serpapi_search
        web_result = serpapi_search(query)
        answer = f"No sufficient answer found in knowledge base.\n\nWeb Result:\n{web_result}"

    # Replace typing bubble with real message
    placeholder.markdown(f'<div class="bot-msg">{answer}</div>', unsafe_allow_html=True)

    # Append assistant message
    chat.append({"role": "assistant", "content": answer})
