import os
from groq import Groq
import chromadb
from utils.embedder import embed

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection("pubmed_articles")

groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))


def answer_question(question: str):
    """Embed the question, retrieve top-2 chunks, ask the LLM, return (answer, chunks)."""
    query_vector = embed(question)
    results = collection.query(query_embeddings=[query_vector], n_results=2)

    chunks = results["metadatas"][0] if results["metadatas"] else []
    context = "\n\n".join(c["context"] for c in chunks)

    if not context:
        return "I don't have any relevant information ingested yet. Try adding a PubMed article first.", []

    prompt = (
        "Answer the question using only the context below. "
        "If the answer isn't in the context, say you don't know.\n\n"
        "Context:\n" + context + "\n\n"
        "Question: " + question
    )

    response = groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
    )
    answer = response.choices[0].message.content

    return answer, [c["context"] for c in chunks]


if __name__ == "__main__":
    q = input("Ask a question: ")
    answer, chunks = answer_question(q)
    print("\nANSWER:\n", answer)
    print("\nSOURCES USED:\n", chunks)
