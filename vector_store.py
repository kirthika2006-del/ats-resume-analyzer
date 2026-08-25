import chromadb

chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection(name="resume_jd_store")


def store_chunks(doc_id, text):
    chunks = [text[i:i + 500] for i in range(0, len(text), 500)]
    for idx, chunk in enumerate(chunks):
        collection.add(
            documents=[chunk],
            ids=[f"{doc_id}_{idx}"]
        )


def retrieve_relevant_chunks(query, n=3):
    results = collection.query(query_texts=[query], n_results=n)
    return " ".join(results["documents"][0]) if results["documents"] else ""
