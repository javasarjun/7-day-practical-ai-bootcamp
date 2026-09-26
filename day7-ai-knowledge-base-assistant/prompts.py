def build_knowledge_base_prompt(question, retrieved_chunks):
    context_blocks = []

    for index, chunk in enumerate(retrieved_chunks, start=1):
        metadata = chunk["metadata"]

        source = (
            f"Source {index}: "
            f"{metadata.get('file_name', 'Unknown file')}, "
            f"Page {metadata.get('page_number', 'Unknown page')}, "
            f"Chunk {metadata.get('chunk_number', 'Unknown chunk')}"
        )

        context_blocks.append(
            f"""
{source}

{chunk["text"]}
"""
        )

    context = "\n\n".join(context_blocks)

    return f"""
You are an AI Knowledge Base Assistant.

Your task:
Answer the user's question using only the provided knowledge base context.

Rules:
- Use only the context provided.
- Do not invent facts.
- If the answer is not in the context, say:
  "I could not find this information in the uploaded knowledge base."
- Keep the answer clear and practical.
- Include source references using file name and page number.
- If multiple sources support the answer, mention them.

User question:
{question}

Knowledge base context:
{context}

Output format:

## Answer

## Source References

## Confidence Note
Explain briefly whether the answer was directly found or partially inferred from the provided context.
"""
