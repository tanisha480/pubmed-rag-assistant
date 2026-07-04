import hashlib
import chromadb
from utils.scraper import scrape_pubmed
from utils.chunker import chunk_text
from utils.embedder import embed

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection("pubmed_articles")


def ingest_url(url: str) -> int:
    """Scrape, chunk, embed, and store a PubMed URL. Returns number of chunks added."""
    text = scrape_pubmed(url)
    if not text:
        raise ValueError("Could not fetch or parse that URL.")

    chunks = chunk_text(text)
    url_hash = hashlib.md5(url.encode()).hexdigest()[:8]

    for i, chunk in enumerate(chunks):
        vector = embed(chunk)
        collection.add(
            ids=[f"{url_hash}_{i}"],
            embeddings=[vector],
            metadatas=[{"title": url, "context": chunk}],
        )

    return len(chunks)


if __name__ == "__main__":
    # Quick manual test: run "python ingest.py" directly to test without the UI
    test_url = input("Paste a PubMed URL to test ingestion: ")
    n = ingest_url(test_url)
    print(f"Added {n} chunks.")