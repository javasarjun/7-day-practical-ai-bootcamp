import streamlit as st

from llm_service import ask_ai
from document_service import extract_text_from_pdf, create_document_chunks
from rag_service import store_chunks, retrieve_relevant_chunks
from rag_prompts import build_rag_prompt


st.set_page_config(
    page_title="Day 4 PDF Chat Assistant",
    page_icon="📚",
    layout="wide",
)

st.title("📚 Day 4: PDF Chat Assistant using RAG")
st.write(
    "Upload a PDF, ask questions, and get answers grounded in your document."
)


# -----------------------------
# Sidebar
# -----------------------------

st.sidebar.title("RAG Pipeline")
st.sidebar.write(
    """
This app follows a simple RAG flow:

1. Upload PDF  
2. Extract text  
3. Split into chunks  
4. Store chunks in ChromaDB  
5. Retrieve relevant chunks  
6. Send context to LLM  
7. Generate grounded answer  
"""
)

st.sidebar.markdown("---")
st.sidebar.subheader("Beginner Note")
st.sidebar.write(
    """
RAG means Retrieval-Augmented Generation.

Instead of asking the LLM to answer from memory, we first retrieve relevant text from our document and then ask the LLM to answer using that text.
"""
)


# -----------------------------
# Session State
# -----------------------------

if "document_ready" not in st.session_state:
    st.session_state.document_ready = False

if "file_name" not in st.session_state:
    st.session_state.file_name = ""

if "chunk_count" not in st.session_state:
    st.session_state.chunk_count = 0

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# -----------------------------
# Upload PDF
# -----------------------------

uploaded_file = st.file_uploader(
    "Upload a PDF document",
    type=["pdf"],
)

if uploaded_file is not None:
    st.info(f"Uploaded file: {uploaded_file.name}")

    if st.button("Process PDF", type="primary"):
        with st.spinner("Extracting text and building document index..."):
            pages = extract_text_from_pdf(uploaded_file)
            chunks = create_document_chunks(pages, uploaded_file.name)
            chunk_count = store_chunks(chunks)

        st.session_state.document_ready = True
        st.session_state.file_name = uploaded_file.name
        st.session_state.chunk_count = chunk_count
        st.session_state.chat_history = []

        st.success(
            f"Document processed successfully. "
            f"{chunk_count} chunks stored in ChromaDB."
        )


# -----------------------------
# Document Status
# -----------------------------

st.markdown("---")
st.subheader("Document Status")

if st.session_state.document_ready:
    st.success("Document is ready for questions.")
    st.write(f"File: {st.session_state.file_name}")
    st.write(f"Chunks stored: {st.session_state.chunk_count}")
else:
    st.warning("Please upload and process a PDF first.")


# -----------------------------
# Chat Section
# -----------------------------

st.markdown("---")
st.subheader("Ask Questions About Your PDF")

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

question = st.chat_input("Ask a question about the uploaded PDF...")

if question:
    if not st.session_state.document_ready:
        st.warning("Please upload and process a PDF before asking questions.")
    else:
        st.session_state.chat_history.append(
            {
                "role": "user",
                "content": question,
            }
        )

        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            with st.spinner("Retrieving relevant context and generating answer..."):
                retrieved_chunks = retrieve_relevant_chunks(question, top_k=4)
                prompt = build_rag_prompt(question, retrieved_chunks)

                messages = [
                    {
                        "role": "system",
                        "content": (
                            "You are a careful RAG assistant. "
                            "Answer only using the retrieved document context."
                        ),
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ]

                answer = ask_ai(messages)

                st.markdown(answer)

                with st.expander("View Retrieved Context"):
                    for index, chunk in enumerate(retrieved_chunks, start=1):
                        metadata = chunk["metadata"]
                        st.markdown(
                            f"### Chunk {index} — Page {metadata.get('page_number')}"
                        )
                        st.write(chunk["text"])

        st.session_state.chat_history.append(
            {
                "role": "assistant",
                "content": answer,
            }
        )


# -----------------------------
# Clear Chat
# -----------------------------

st.markdown("---")

if st.button("Clear Chat"):
    st.session_state.chat_history = []
    st.rerun()


# -----------------------------
# Footer
# -----------------------------

st.caption(
    "Day 4 Lab: This is a beginner-friendly RAG app for learning document Q&A."
)
