import re

# In-memory document store
documents_store = {}


def split_into_chunks(text, chunk_size=500):
    """Split text into small chunks."""
    text = text.strip()

    if not text:
        return []

    return [
        text[i:i + chunk_size]
        for i in range(0, len(text), chunk_size)
    ]


def store_chunks(doc_id, text):
    """Store document chunks in memory."""
    documents_store[doc_id] = split_into_chunks(text)


def retrieve_relevant_chunks(query, n=3):
    """Retrieve chunks containing the most query keywords."""

    if not query:
        return ""

    query_words = set(
        re.findall(r"\b[a-zA-Z0-9+#.-]{2,}\b", query.lower())
    )

    all_chunks = []

    for doc_id, chunks in documents_store.items():
        for chunk in chunks:
            chunk_words = set(
                re.findall(
                    r"\b[a-zA-Z0-9+#.-]{2,}\b",
                    chunk.lower()
                )
            )

            score = len(query_words & chunk_words)

            all_chunks.append((score, chunk))

    # Highest matching chunks first
    all_chunks.sort(key=lambda x: x[0], reverse=True)

    selected = [
        chunk for score, chunk in all_chunks[:n]
        if score > 0
    ]

    return " ".join(selected)