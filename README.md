

# Egypt Tour Guide Chatbot

## Overview

This project is an interactive chatbot application designed to provide users with detailed information and guidance about tourism in Egypt. It leverages a combination of a knowledge base extracted from a PDF, vector search embeddings, and a large language model (LLM) to answer questions effectively. If the internal knowledge base cannot provide a satisfactory answer, the chatbot automatically queries the web via SerpAPI to deliver relevant information.

The application is built with Streamlit for an intuitive web interface and supports multiple chat sessions with persistent history and chat titles derived from user queries.

---

## Features

* **PDF-based Knowledge Extraction:** Parses a custom Egypt tourism PDF and indexes its content for efficient retrieval.
* **Vector Search with Embeddings:** Uses sentence-transformer embeddings and Chroma vector store for similarity search.
* **Large Language Model Integration:** Employs a locally hosted or remote LLM to generate natural language answers.
* **Web Search Fallback:** Integrates SerpAPI for live web results if the internal knowledge base cannot answer the query.
* **Session Management:** Supports multiple chat sessions with saving, loading, and titling based on conversation content.
* **Dark Themed UI:** Custom CSS styling for a clean, dark-themed chat interface.
* **Typing Indicator:** Shows a typing bubble during LLM response generation for better UX.
* **User and Bot Message Icons:** Distinct icons to differentiate between user and assistant messages.
* **Streamlit Interface:** Easy deployment and interaction with a modern web app framework.

---

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/Habiba480/egypt-tour-guide-chatbot.git
   cd egypt-tour-guide-chatbot
   ```

2. **Create and activate a Python virtual environment (optional but recommended)**

   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/macOS
   venv\Scripts\activate      # Windows
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables**

   Create a `.env` file in the root directory and add your SerpAPI key:

   ```
   SERPAPI_API_KEY=your_serpapi_api_key_here
   ```

5. **Prepare the PDF knowledge base**

   Ensure the file `Egypt Tour Guide Knowledge Base.pdf` is placed in the project root directory.

6. **Run the application**

   ```bash
   streamlit run app.py
   ```

---

## Usage

* Start the app and ask any question related to Egypt tourism.
* Your queries will be answered using the internal knowledge base indexed from the PDF.
* If no satisfactory answer is found internally, the app will fetch relevant web results via SerpAPI.
* Use the sidebar to manage multiple chat sessions:

  * Click "New Chat" to save the current conversation and start a fresh chat.
  * Select any saved chat from the sidebar and load it for review or continuation.
* Chat titles are automatically generated from the first user message in each session.

---

## Code Structure

* **`app.py`**: Main Streamlit application script containing UI, session management, chatbot logic, and integration with LLM and vector database.
* **`Egypt Tour Guide Knowledge Base.pdf`**: Source PDF containing Egypt tourism information.
* **`./egypt_guide_db/`**: Directory where the vectorstore database is persisted.
* **`.env`**: Environment variable file holding sensitive API keys.

---

## Dependencies

* Python 3.8+
* Streamlit
* PyMuPDF (`fitz`)
* LangChain (core, chat\_models, embeddings, chains)
* Chroma vector store
* Sentence Transformers (`sentence-transformers/all-MiniLM-L6-v2`)
* SerpAPI Python client
* python-dotenv

See `requirements.txt` for exact versions.

---

## Environment Variables

* `SERPAPI_API_KEY`: Your API key for SerpAPI, used for fallback web searches.

---

## Customization

* You can update the PDF knowledge base with your own documents by replacing the PDF file.
* Change the LLM model or API endpoint by modifying the `ChatOpenAI` instantiation.
* Adjust chunk sizes or embeddings model for vectorstore indexing as needed.

---

## License

MIT License.

---




