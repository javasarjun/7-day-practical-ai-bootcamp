import chromadb


CHROMA_DB_PATH = "chroma_db"
COLLECTION_NAME = "pdf_chat_collection"


client = chromadb.PersistentClient(path=CHROMA_DB_PATH)


def get_or_create_collection():
    """
    Creates or loads a ChromaDB collection.
    """

    return client.get_or_create_collection(name=COLLECTION_NAME)


def clear_collection():
    """
    Deletes and recreates the collection.
    Useful when uploading a new PDF for the beginner lab.
    """

    try:
        client.delete_collection(name=COLLECTION_NAME)
    except Exception:
        pass

    return client.get_or_create_collection(name=COLLECTION_NAME)


def store_chunks(chunks):
    """
    Stores document chunks in ChromaDB.
    ChromaDB will create embeddings for the text and store metadata.
    """

    collection = clear_collection()

    ids = []
    documents = []
    metadatas = []

    for chunk in chunks:
        ids.append(chunk["id"])
        documents.append(chunk["text"])
        metadatas.append(chunk["metadata"])

    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas,
    )

    return len(ids)


def retrieve_relevant_chunks(question, top_k=4):
    """
    Searches ChromaDB for chunks most relevant to the user's question.
    """

    collection = get_or_create_collection()

    results = collection.query(
        query_texts=[question],
        n_results=top_k,
    )

    retrieved_chunks = []

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]

    for document, metadata in zip(documents, metadatas):
        retrieved_chunks.append(
            {
                "text": document,
                "metadata": metadata,
            }
        )

    return retrieved_chunks
