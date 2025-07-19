import streamlit as st
from src.state import get_current_chat

def render_custom_style():
    st.markdown("""
    <style>
        body, .stApp {
            background-color: #0d0d0d;
            color: #f5f5f5;
        }

        .user-msg {
            background-color: #1a1a1a;
            color: #eaeaea;
            border-radius: 12px;
            padding: 12px;
            margin-bottom: 8px;
            max-width: 70%;
            align-self: flex-end;
        }

        .bot-msg {
            background-color: #262626;
            color: #f0f0f0;
            border-radius: 12px;
            padding: 12px;
            margin-bottom: 8px;
            max-width: 70%;
            align-self: flex-start;
        }

        .typing-bubble {
            background-color: #1f1f1f;
            color: #aaaaaa;
            font-style: italic;
            border-radius: 10px;
            padding: 8px 12px;
            margin-bottom: 10px;
            max-width: fit-content;
            align-self: flex-start;
        }

        .chat-container {
            display: flex;
            flex-direction: column;
            gap: 12px;
        }
    </style>
    """, unsafe_allow_html=True)

def display_chat():
    chat = get_current_chat()
    for msg in chat[1:]:  # skip system prompt
        css_class = "user-msg" if msg["role"] == "user" else "bot-msg"
        st.markdown(f'<div class="{css_class}">{msg["content"]}</div>', unsafe_allow_html=True)
