# PubMed RAG Assistant

A local RAG (Retrieval-Augmented Generation) app that ingests PubMed articles and answers questions about them using a locally-running LLM (Ollama), ChromaDB for vector search, and a Streamlit UI.

## Features
- Fully local — no API keys, no data leaves your machine
- Fetches PubMed abstracts via NCBI's official API
- Answers grounded in retrieved context (shows sources)

## Prerequisites
- Python 3.10+
- [Ollama](https://ollama.com) installed with a model pulled (e.g. `llama3.2:1b`)

## Setup
\`\`\`bash
git clone https://github.com/tanisha480/pubmed-rag-assistant.git
cd pubmed-rag-assistant
python -m venv venv
venv\Scripts\activate   # Mac/Linux: source venv/bin/activate
pip install -r requirements.txt
ollama pull llama3.2:1b
\`\`\`

## Usage
\`\`\`bash
streamlit run main.py
\`\`\`
Open http://localhost:8501, paste a PubMed URL in "Update Database", then ask questions in "Ask a Question".

## License
MIT