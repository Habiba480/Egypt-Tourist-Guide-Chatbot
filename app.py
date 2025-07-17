import os
import asyncio
import streamlit as st
from dotenv import load_dotenv

from langchain.chains import LLMChain, RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda, RunnableMap, RunnableConfig
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import HumanMessage, AIMessage

from langchain_community.chat_message_histories.streamlit import StreamlitChatMessageHistory
from langchain_community.utilities import SerpAPIWrapper
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI

# === ENV setup ===
os.environ["TOKENIZERS_PARALLELISM"] = "false"
load_dotenv()

# === Set API keys ===
os.environ["SERPAPI_API_KEY"] = os.getenv("SERPAPI_API_KEY")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_BASE"] = os.getenv("OPENAI_API_BASE") or "https://api.together.xyz/v1"

# === Async fix for Streamlit ===
try:
    asyncio.get_event_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

# === Initialize HuggingFace Embeddings ===
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# === Load and preprocess docs ===
@st.cache_resource
def load_data():
    file_path = "/Users/habiba/PycharmProjects/RAGs project/egypt_rag_guide.txt"
    loader = TextLoader(file_path)
    docs = loader.load()
    docs = [doc for doc in docs if doc.page_content.strip()]

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = splitter.split_documents(docs)
    return Chroma.from_documents(splits, embeddings)

vectorstore = load_data()
retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 5})

# === Initialize Together API LLM ===
llm = ChatOpenAI(
    model="mistralai/Mixtral-8x7B-Instruct-v0.1",
    temperature=0,

)

# === SerpAPI wrapper ===
serpapi_tool = SerpAPIWrapper(serpapi_api_key=os.getenv("SERPAPI_API_KEY"))

# === Custom prompt ===
prompt_template = """
You are an expert Egyptian tourism guide. Provide clear, engaging, and accurate answers about Egypt's history, travel tips, logistics, and more.

Context:
{context}

Question:
{question}

Answer:
"""

prompt = PromptTemplate(
    template=prompt_template,
    input_variables=["context", "question"]
)

# === Retrieval QA Chain ===
retrieval_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    chain_type="stuff",
    return_source_documents=False,
    chain_type_kwargs={"prompt": prompt}
)

# === Smart routing logic ===
def smart_router(inputs):
    question = inputs["input"]
    docs = retriever.invoke({"input": question})
    if docs:
        return {"source": "rag", "question": question}
    return {"source": "serpapi", "question": question}

router = RunnableLambda(smart_router)

# === LLM + Retrieval Lambda chains ===
serpapi_chain = RunnableLambda(lambda x: {"result": serpapi_tool.run(x["question"])})

rag_chain = RunnableLambda(lambda x: {
    "result": retrieval_chain.invoke({"query": x["question"]})
})

final_chain = router | RunnableMap({
    "rag": rag_chain,
    "serpapi": serpapi_chain,
})

# === Chat memory handler ===
chat_history = StreamlitChatMessageHistory(key="egypt_tour_chat")

chat_runnable = RunnableWithMessageHistory(
    final_chain,
    lambda session_id: chat_history,
    input_messages_key="input",
    history_messages_key="chat_history",
)

# === Streamlit UI ===
st.set_page_config(page_title="Egypt Tourist Guide 🇪🇬", layout="wide")
st.title("🇪🇬 Egypt Tourist Guide Chatbot")
st.markdown("Ask anything about Egypt’s history, sites, culture, or travel info!")

prompt_text = st.chat_input("Where do you want to go in Egypt?")

if prompt_text:
    st.chat_message("user").write(prompt_text)

    # === Debug retrieval and LLM separately ===
    if st.button("🔍 Debug Retrieval & LLM for this query"):
        docs = retriever.invoke({"input": prompt_text})
        st.write(f"🔎 Found {len(docs)} relevant chunks:")
        for i, doc in enumerate(docs):
            st.write(f"--- Doc {i + 1} ---")
            st.write(doc.page_content[:500])

        if docs:
            result = retrieval_chain.invoke({"query": prompt_text})
            st.write("### 💬 LLM Answer:")
            st.write(result)
        else:
            st.warning("No relevant documents found.")

    # === Normal chat flow ===
    response = chat_runnable.invoke(
        {"input": prompt_text},
        config=RunnableConfig(configurable={"session_id": "egypt_guide_session"})
    )
    if "result" in response and response["result"].strip():
        st.chat_message("assistant").write(response["result"])
    else:
        st.chat_message("assistant").write("Sorry, I couldn't find relevant info.")

# === Replay chat history ===
for msg in chat_history.messages:
    with st.chat_message("user" if isinstance(msg, HumanMessage) else "assistant"):
        st.write(msg.content)
