import uuid
import streamlit as st
from src.config import SYSTEM_PROMPT

def init_chat_state():
    if "chat_sessions" not in st.session_state:
        st.session_state.chat_sessions = {}

    if "current_session_id" not in st.session_state:
        sid = str(uuid.uuid4())
        st.session_state.current_session_id = sid
        st.session_state.chat_sessions[sid] = [{"role": "system", "content": SYSTEM_PROMPT}]

def get_current_chat():
    sid = st.session_state.current_session_id
    return st.session_state.chat_sessions[sid]

def switch_chat(sid):
    st.session_state.current_session_id = sid

def new_chat():
    sid = str(uuid.uuid4())
    st.session_state.current_session_id = sid
    st.session_state.chat_sessions[sid] = [{"role": "system", "content": SYSTEM_PROMPT}]
