import streamlit as st
from ingest import ingest_url
from query import answer_question

st.set_page_config(page_title="PubMed RAG Assistant")
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
    question = st.text_input("Your question")
    if st.button("Ask"):
        if not question:
            st.warning("Please type a question first.")
        else:
            with st.spinner("Thinking..."):
                answer, chunks = answer_question(question)
            st.write(answer)
            if chunks:
                with st.expander("Show retrieved context"):
                    for c in chunks:
                        st.write(c)
                        st.divider()