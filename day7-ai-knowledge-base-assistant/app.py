import streamlit as st

from llm_service import ask_ai
from document_service import extract_text_from_pdf, create_chunks_from_pages
from rag_service import (
    reset_knowledge_base,
    store_chunks,
    retrieve_relevant_chunks,
)
from prompts import build_knowledge_base_prompt


st.set_page_config(
    page_title="AI Knowledge Base Assistant",
    page_icon="🧠",
    layout="wide",
)

st.title("🧠 AI Knowledge Base Assistant")
st.write(
    "Upload PDF documents, build a knowledge base, and ask grounded questions."
)


# -----------------------------
# Session State
# -----------------------------

if "knowledge_base_ready" not in st.session_state:
    st.session_state.knowledge_base_ready = False

if "processed_files" not in st.session_state:
    st.session_state.processed_files = []

if "total_chunks" not in st.session_state:
    st.session_state.total_chunks = 0

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# -----------------------------
# Sidebar
# -----------------------------

st.sidebar.title("Capstone Project")
st.sidebar.write(
    """
This app combines:

- LLM calls
- Prompt engineering
- PDF processing
- RAG
- Vector search
- Streamlit UI
- Docker deployment
"""
)

st.sidebar.markdown("---")

top_k = st.sidebar.slider(
    "Number of chunks to retrieve",
    min_value=1,
    max_value=8,
    value=4,
)

show_context = st.sidebar.checkbox(
    "Show retrieved context",
    value=True,
)

st.sidebar.markdown("---")

if st.sidebar.button("Clear Knowledge Base"):
    reset_knowledge_base()
    st.session_state.knowledge_base_ready = False
    st.session_state.processed_files = []
    st.session_state.total_chunks = 0
    st.session_state.chat_history = []
    st.sidebar.success("Knowledge base cleared.")


# -----------------------------
# Upload Documents
# -----------------------------

st.subheader("1. Upload Knowledge Base Documents")

uploaded_files = st.file_uploader(
    "Upload one or more PDF files",
    type=["pdf"],
    accept_multiple_files=True,
)

if uploaded_files:
    if st.button("Build Knowledge Base", type="primary"):
        with st.spinner("Processing PDFs and building knowledge base..."):
            reset_knowledge_base()

            total_chunks = 0
            processed_files = []

            for uploaded_file in uploaded_files:
                pages = extract_text_from_pdf(uploaded_file)
                chunks = create_chunks_from_pages(
                    pages=pages,
                    file_name=uploaded_file.name,
                )

                chunk_count = store_chunks(chunks)

                total_chunks += chunk_count
                processed_files.append(uploaded_file.name)

            st.session_state.knowledge_base_ready = True
            st.session_state.processed_files = processed_files
            st.session_state.total_chunks = total_chunks
            st.session_state.chat_history = []

        st.success(
            f"Knowledge base built successfully with {total_chunks} chunks."
        )


# -----------------------------
# Knowledge Base Status
# -----------------------------

st.markdown("---")
st.subheader("2. Knowledge Base Status")

if st.session_state.knowledge_base_ready:
    st.success("Knowledge base is ready.")

    st.write("Processed files:")

    for file_name in st.session_state.processed_files:
        st.write(f"- {file_name}")

    st.write(f"Total chunks stored: {st.session_state.total_chunks}")
else:
    st.warning("Upload PDF files and build the knowledge base first.")


# -----------------------------
# Chat
# -----------------------------

st.markdown("---")
st.subheader("3. Ask Questions")

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

question = st.chat_input("Ask a question about your knowledge base...")

if question:
    if not st.session_state.knowledge_base_ready:
        st.warning("Please build the knowledge base before asking questions.")
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
            with st.spinner("Retrieving context and generating answer..."):
                retrieved_chunks = retrieve_relevant_chunks(
                    question=question,
                    top_k=top_k,
                )

                prompt = build_knowledge_base_prompt(
                    question=question,
                    retrieved_chunks=retrieved_chunks,
                )

                messages = [
                    {
                        "role": "system",
                        "content": (
                            "You are a careful AI assistant. "
                            "Answer only using the provided knowledge base context."
                        ),
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ]

                answer = ask_ai(messages)

                st.markdown(answer)

                if show_context:
                    with st.expander("Retrieved Context"):
                        for index, chunk in enumerate(retrieved_chunks, start=1):
                            metadata = chunk["metadata"]

                            st.markdown(
                                f"### Chunk {index}: "
                                f"{metadata.get('file_name')} — "
                                f"Page {metadata.get('page_number')}"
                            )

                            st.caption(
                                f"Similarity distance: {chunk.get('distance')}"
                            )

                            st.write(chunk["text"])

        st.session_state.chat_history.append(
            {
                "role": "assistant",
                "content": answer,
            }
        )


# -----------------------------
# Download Chat
# -----------------------------

st.markdown("---")
st.subheader("4. Export")

if st.session_state.chat_history:
    chat_text = ""

    for message in st.session_state.chat_history:
        role = message["role"].upper()
        content = message["content"]
        chat_text += f"\n\n## {role}\n\n{content}"

    st.download_button(
        label="Download Chat History",
        data=chat_text,
        file_name="knowledge_base_chat.md",
        mime="text/markdown",
    )
else:
    st.info("Ask at least one question to enable chat export.")


# -----------------------------
# Footer
# -----------------------------

st.markdown("---")
st.caption(
    "Capstone Lab: AI Knowledge Base Assistant using Python, Streamlit, ChromaDB, and an LLM."
)
