from pypdf import PdfReader


def extract_text_from_pdf(uploaded_file):
    """
    Extracts text from an uploaded PDF file.
    Returns a list of page dictionaries.
    """

    reader = PdfReader(uploaded_file)
    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        page_text = page.extract_text()

        if page_text and page_text.strip():
            pages.append(
                {
                    "page_number": page_number,
                    "text": page_text.strip(),
                }
            )

    return pages


def chunk_text(text, chunk_size=900, overlap=150):
    """
    Splits text into overlapping chunks.

    Example:
    chunk_size = 900 characters
    overlap = 150 characters

    This means each chunk shares a small amount of text
    with the previous chunk, which helps preserve context.
    """

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]

        if chunk.strip():
            chunks.append(chunk.strip())

        start = end - overlap

    return chunks


def create_document_chunks(pages, file_name):
    """
    Converts PDF pages into searchable chunks.
    Each chunk keeps metadata like file name and page number.
    """

    all_chunks = []

    for page in pages:
        page_number = page["page_number"]
        page_text = page["text"]

        chunks = chunk_text(page_text)

        for chunk_index, chunk in enumerate(chunks, start=1):
            all_chunks.append(
                {
                    "id": f"{file_name}_page_{page_number}_chunk_{chunk_index}",
                    "text": chunk,
                    "metadata": {
                        "file_name": file_name,
                        "page_number": page_number,
                        "chunk_number": chunk_index,
                    },
                }
            )

    return all_chunks
