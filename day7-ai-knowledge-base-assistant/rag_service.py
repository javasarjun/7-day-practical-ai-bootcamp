import chromadb


CHROMA_DB_PATH = "chroma_db"
COLLECTION_NAME = "knowledge_base"

client = chromadb.PersistentClient(path=CHROMA_DB_PATH)


def get_collection():
    return client.get_or_create_collection(name=COLLECTION_NAME)


def reset_knowledge_base():
    try:
        client.delete_collection(name=COLLECTION_NAME)
    except Exception:
        pass

    return client.get_or_create_collection(name=COLLECTION_NAME)


def store_chunks(chunks):
    collection = get_collection()

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
    collection = get_collection()

    results = collection.query(
        query_texts=[question],
        n_results=top_k,
    )

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    chunks = []

    for document, metadata, distance in zip(documents, metadatas, distances):
        chunks.append(
            {
                "text": document,
                "metadata": metadata,
                "distance": distance,
            }
        )

    return chunks
