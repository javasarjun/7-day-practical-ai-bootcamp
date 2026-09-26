from pypdf import PdfReader


def extract_text_from_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text()

        if text and text.strip():
            pages.append(
                {
                    "page_number": page_number,
                    "text": text.strip(),
                }
            )

    return pages


def chunk_text(text, chunk_size=900, overlap=150):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]

        if chunk.strip():
            chunks.append(chunk.strip())

        start = end - overlap

    return chunks


def create_chunks_from_pages(pages, file_name):
    chunks = []

    for page in pages:
        page_number = page["page_number"]
        page_text = page["text"]

        page_chunks = chunk_text(page_text)

        for chunk_index, chunk in enumerate(page_chunks, start=1):
            chunk_id = f"{file_name}_page_{page_number}_chunk_{chunk_index}"

            chunks.append(
                {
                    "id": chunk_id,
                    "text": chunk,
                    "metadata": {
                        "file_name": file_name,
                        "page_number": page_number,
                        "chunk_number": chunk_index,
                    },
                }
            )

    return chunks
