
# Egypt Tourist Guide Chatbot

This project is an AI-powered chatbot designed to serve as a virtual Egyptian tourism guide. It uses **LangChain**, **OpenAI-compatible LLMs**, **Hugging Face embeddings**, and a **local vectorstore (Chroma)** to answer user questions related to Egyptian history, travel logistics, tourist sites, culture, and more.

The chatbot supports both **retrieval-augmented generation (RAG)** from a local corpus and **fallback web search** using SerpAPI. It runs as a **Streamlit web app** with persistent chat memory.

---

## Features

* Retrieval-based QA using vector search and Mistral LLMs via Together API
* Web search fallback using SerpAPI
* Multi-turn conversation with persistent chat history
* Streamlit-based UI
* Modular and extendable architecture using LangChain runnables
* HuggingFace sentence transformer embeddings for document indexing

---

## Project Structure

```
egypt_guide_chatbot/
├── egypt_rag_guide.txt           # Source document for vector search
├── main_app.py                   # Main Streamlit application script
├── .env                          # API keys and environment variables
├── requirements.txt              # Python dependencies
```

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/egypt-tour-guide-chatbot.git
cd egypt-tour-guide-chatbot
```

### 2. Create and Activate Virtual Environment

```bash
python -m venv env
source env/bin/activate  # On Windows use `env\Scripts\activate`
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file with the following:

```env
OPENAI_API_KEY=your_openai_or_together_api_key
OPENAI_API_BASE=https://api.together.xyz/v1
SERPAPI_API_KEY=your_serpapi_key
```

### 5. Add Your Corpus

Replace or update `egypt_rag_guide.txt` with your curated text file containing tourism-related content about Egypt.

---

## Run the App

```bash
streamlit run main_app.py
```

The app will launch in your browser. You can ask questions such as:

* “What are the best places to visit in Aswan?”
* “When is the best time to visit Luxor?”
* “What are the visa requirements for tourists in Egypt?”

---

## Tech Stack

* **LangChain**: Framework for building LLM-powered apps
* **Streamlit**: UI and frontend
* **Chroma**: Local vector database for retrieval
* **HuggingFace Embeddings**: `all-MiniLM-L6-v2`
* **Together API**: Used to access Mistral 8x7B Instruct model
* **SerpAPI**: Web search fallback for out-of-domain queries

---

## Customization

* To update the LLM, change the `ChatOpenAI` model parameters.
* To add more documents, modify `egypt_rag_guide.txt` and restart the app.
* To extend logic, edit or add new branches in the `smart_router` function.

---

## Known Issues

* Requires internet access for LLM and SerpAPI
* Limited to the quality and scope of the `egypt_rag_guide.txt` document
* Ensure `.env` keys are valid to avoid runtime errors

---

## License

This project is released under the [MIT License](LICENSE).

