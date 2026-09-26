def build_rag_prompt(question, retrieved_chunks):
    """
    Builds a grounded RAG prompt using retrieved document chunks.
    """

    context_sections = []

    for index, chunk in enumerate(retrieved_chunks, start=1):
        metadata = chunk["metadata"]

        source_label = (
            f"Source {index}: "
            f"{metadata.get('file_name', 'Unknown file')}, "
            f"Page {metadata.get('page_number', 'Unknown page')}, "
            f"Chunk {metadata.get('chunk_number', 'Unknown chunk')}"
        )

        context_sections.append(
            f"""
{source_label}

{chunk["text"]}
"""
        )

    context = "\n\n".join(context_sections)

    return f"""
You are a helpful document question-answering assistant.

Your task:
Answer the user's question using only the provided document context.

Rules:
- Use only the context provided below.
- If the answer is not present in the context, say:
  "I could not find this information in the uploaded document."
- Do not make up facts.
- Keep the answer clear and practical.
- Include source references using page numbers when possible.

User question:
{question}

Document context:
{context}

Output format:

## Answer

## Source References
- File name, page number, and chunk number used
"""
