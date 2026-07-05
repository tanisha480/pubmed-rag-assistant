import streamlit as st
from ingest import ingest_url
from query import answer_question

st.set_page_config(page_title="PubMed RAG Assistant", page_icon="🧬", layout="wide")

st.markdown("""
<style>
.stApp {
    background: linear-gradient(-45deg, #0E1117, #1A1D29, #2B1B3D, #0E1117);
    background-size: 400% 400%;
    animation: gradientShift 15s ease infinite;
}
@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
.stButton button {
    background-color: #FF5C8A;
    color: white;
    border-radius: 8px;
    border: none;
    padding: 0.5rem 1.5rem;
    font-weight: 600;
}
.stButton button:hover {
    background-color: #E04A75;
    color: white;
}
div[data-testid="stExpander"] {
    border: 1px solid #FF5C8A;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("About")
    st.write(
        "This app answers questions about PubMed articles using a local "
        "vector database (ChromaDB) and Groq's LLM."
    )
    st.write("---")
    st.write("**How to use:**")
    st.write("1. Paste a PubMed URL in 'Update Database'")
    st.write("2. Click Ingest")
    st.write("3. Ask a question about it")

st.title("PubMed RAG Assistant")

tab1, tab2 = st.tabs(["Update Database", "Ask a Question"])

with tab1:
    st.subheader("Add a PubMed article to the database")
    url = st.text_input("PubMed URL", placeholder="https://pubmed.ncbi.nlm.nih.gov/12345678/")
    if st.button("Ingest"):
        if not url:
            st.warning("Please paste a URL first.")
        else:
            with st.spinner("Scraping, chunking, embedding..."):
                try:
                    n_chunks = ingest_url(url)
                    st.success(f"Added {n_chunks} chunks to the database.")
                except Exception as e:
                    st.error(f"Something went wrong: {e}")

with tab2:
    st.subheader("Ask a question about ingested articles")

    col1, col2 = st.columns([3, 1])
    with col1:
        question = st.text_input("Your question")
    with col2:
        st.write("")
        st.write("")
        ask_clicked = st.button("Ask")

    if ask_clicked:
        if not question:
            st.warning("Please type a question first.")
        else:
            with st.spinner("Thinking..."):
                answer, chunks = answer_question(question)

            st.markdown("### Answer")
            st.info(answer)

            if chunks:
                with st.expander("Show retrieved context"):
                    for c in chunks:
                        st.write(c)
                        st.divider()
