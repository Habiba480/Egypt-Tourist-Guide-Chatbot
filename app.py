import os
import fitz
import streamlit as st
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from serpapi import GoogleSearch
import dotenv
dotenv.load_dotenv()
import streamlit as st

# Initialize session state
if "current_chat" not in st.session_state:
    st.session_state.current_chat = []

if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = []

if "chat_titles" not in st.session_state:
    st.session_state.chat_titles = []

api_key = os.getenv("SERPAPI_API_KEY")

st.set_page_config(page_title="Egypt Tour Guide Chatbot", layout="wide")

@st.cache_resource
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

@st.cache_resource
def load_vectorstore():
    pdf_text = extract_text_from_pdf("Egypt Tour Guide Knowledge Base.pdf")
    doc = Document(page_content=pdf_text)
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents([doc])
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = Chroma.from_documents(chunks, embedding_model, persist_directory="./egypt_guide_db")
    vectorstore.persist()
    return vectorstore

vectorstore = load_vectorstore()

llm = ChatOpenAI(
    base_url="http://0.0.0.0:1234/v1",
    model="meta-llama-3.1-8b-instruct",
    api_key="lm-studio"
)

retriever = vectorstore.as_retriever()
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    chain_type="stuff",
    return_source_documents=True
)

def serpapi_search(query):
    search = GoogleSearch({"q": query, "api_key": api_key})
    results = search.get_dict()
    if "organic_results" in results:
        top = results["organic_results"][0]
        return f"{top['title']}\n{top['snippet']}\n{top['link']}"
    return "No results found from the web."

def ask_tour_guide(question):
    result = qa_chain({"query": question})
    answer = result["result"]
    if "I'm not sure" in answer or len(answer.strip()) < 50:
        web_answer = serpapi_search(question)
        return f"No answer found in internal knowledge base.\n\nWeb Result:\n{web_answer}"
    return answer

# --- UI and state management ---

if "chat_histories" not in st.session_state:
    st.session_state.chat_histories = []
if "current_chat" not in st.session_state:
    st.session_state.current_chat = []

# Styling
st.markdown("""
<style>
    body, .stApp {
        background-color: #0d0d0d; /* Deep black background */
        color: #f5f5f5;            /* Soft white text */
    }

    .user-msg {
        background-color: #1a1a1a; /* Dark gray bubble for user */
        color: #eaeaea;            /* Light gray text */
        border-radius: 12px;
        padding: 12px;
        margin-bottom: 8px;
        max-width: 70%;
        align-self: flex-end;
    }

    .bot-msg {
        background-color: #262626; /* Slightly lighter gray for bot */
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

st.title(" Egypt Tour Guide Chatbot")

# Initialize session state variables if not already set
if "chat_histories" not in st.session_state:
    st.session_state.chat_histories = []

if "current_chat" not in st.session_state:
    st.session_state.current_chat = []

if "active_chat_index" not in st.session_state:
    st.session_state.active_chat_index = None
def generate_chat_title(chat):
    for msg in chat:
        if msg["role"] == "user" and msg["content"].strip():
            return msg["content"][:30] + "..." if len(msg["content"]) > 30 else msg["content"]
    return "Untitled Chat"

with st.sidebar:
    st.header("Chats")

    # Handle new chat button
    if st.button("➕ New Chat"):
        if st.session_state.current_chat:
            title = generate_chat_title(st.session_state.current_chat)
            st.session_state.chat_sessions.append(st.session_state.current_chat)
            st.session_state.chat_titles.append(title)
        st.session_state.current_chat = []
        st.rerun()

    # Only show chat selector if there are saved chats
    if st.session_state.chat_sessions:
        selected_title = st.radio("Select chat", st.session_state.chat_titles, index=len(st.session_state.chat_titles) - 1)

        # Safety check: Make sure the title exists in the list
        if selected_title in st.session_state.chat_titles:
            selected_index = st.session_state.chat_titles.index(selected_title)

            if st.button("🔁 Load Selected Chat"):
                st.session_state.current_chat = st.session_state.chat_sessions[selected_index]
                st.rerun()


# Display chat messages with icons
for msg in st.session_state.current_chat:
    icon = "👤" if msg["role"] == "user" else "🤖"
    css_class = "user-msg" if msg["role"] == "user" else "bot-msg"
    st.markdown(f'<div class="{css_class}">{icon} {msg["content"]}</div>', unsafe_allow_html=True)

# Chat input
query = st.chat_input("Ask me anything about Egypt...")

if query:
    # Save user message to session state
    st.session_state.current_chat.append({"role": "user", "content": query})

    # Display user message immediately
    with st.chat_message("user"):
        st.markdown(f'<div class="user-msg">{query}</div>', unsafe_allow_html=True)

    # Typing indicator placeholder
    with st.chat_message("assistant"):
        typing_placeholder = st.empty()
        typing_placeholder.markdown('<div class="typing-bubble">🤖 is typing...</div>', unsafe_allow_html=True)

    # Get bot response (simulate delay if you want realism)
    response = ask_tour_guide(query)

    # Replace typing bubble with real bot message
    typing_placeholder.markdown(f'<div class="bot-msg">{response}</div>', unsafe_allow_html=True)

    # Save bot message to session state
    st.session_state.current_chat.append({"role": "assistant", "content": response})

