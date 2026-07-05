# PubMed RAG Assistant

A Retrieval-Augmented Generation (RAG) app that lets you paste in PubMed article URLs, stores them in a local vector database, and answers questions about them using an LLM — all through a simple Streamlit UI.

## How it works

1. **Add articles** — Paste a PubMed URL (e.g. `https://pubmed.ncbi.nlm.nih.gov/12345678/`) into the "Update Database" tab and click **Ingest**.
2. **Scrape & chunk** — The app fetches the page with `requests` + `BeautifulSoup`, extracts the article text, and splits it into smaller chunks.
3. **Embed locally** — Each chunk is converted into a vector embedding using `sentence-transformers` (runs locally, no external API call for this step).
4. **Store** — Chunks and embeddings are saved in **ChromaDB**, a local persistent vector database (`./chroma_db`).
5. **Ask questions** — In the "Ask a Question" tab, your question is embedded the same way, the top matching chunks are retrieved from ChromaDB, and that context is sent to **Groq's cloud LLM API** (`llama-3.1-8b-instant`) to generate a grounded answer.

There is **no bulk import and no scheduled updates** — the database only grows when a URL is manually pasted and ingested through the UI. It starts empty and grows one article at a time as URLs are added.

## Tech stack

- **Frontend**: Streamlit
- **Scraping**: `requests` + `beautifulsoup4` (scrapes the public PubMed abstract page — does **not** use NCBI's official Entrez/E-utilities API)
- **Embeddings**: `sentence-transformers` (local)
- **Vector database**: ChromaDB (local, persistent)
- **LLM**: Groq API (`llama-3.1-8b-instant`) — **cloud-based, requires a `GROQ_API_KEY`**

## ⚠️ Note on "local"

This app does **not** run fully locally and does **not** use Ollama. Only the embedding step runs locally — question-answering calls Groq's cloud API. Since this app is deployed publicly, anyone visiting the live URL triggers Groq API calls using the deployed key, so keep an eye on usage/rate limits.

## Prerequisites

- Python 3.10+
- A [Groq API key](https://console.groq.com) (free tier available)

## Setup

bash
git clone https://github.com/tanisha480/pubmed-rag-assistant.git
cd pubmed-rag-assistant
python -m venv venv
venv\Scripts\activate   # Mac/Linux: source venv/bin/activate
pip install -r requirements.txt


Set your Groq API key as an environment variable (or via Streamlit secrets when deploying):

bash
export GROQ_API_KEY=your_key_here   # Mac/Linux
set GROQ_API_KEY=your_key_here      # Windows


## 🔗 Live Demo

Try it here: https://pubmed-rag-assistant-jjuqbaasjlfdarhesapprxq.streamlit.app/

## Usage (running locally)

If you'd rather run it on your own machine instead of using the live demo above:

bash
streamlit run main.py


This opens the app at http://localhost:8501 (only accessible on your computer). Paste a PubMed URL in **Update Database**, click **Ingest**, then ask questions in **Ask a Question**.

## License

MIT
