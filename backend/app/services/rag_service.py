from app.services.embedding_service import create_embedding
from app.services.qdrant_service import search_chunks

# This function takes a user query, converts it into an embedding, searches the Qdrant database for relevant chunks, and returns the retrieved chunk text as a single context string.
def retrieve_context(query: str) -> str:
    """
    Convert a user query into an embedding,
    search Qdrant, and return the retrieved
    chunk text as a single context string.
    """

    query_embedding = create_embedding(query)

    results = search_chunks(query_embedding)

    context = "\n\n".join(
        result.payload["text"]
        for result in results
    )

    return context