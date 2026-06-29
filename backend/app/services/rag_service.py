from app.services.embedding_service import create_embedding
from app.services.qdrant_service import search_chunks
from app.services.llm_service import generate_answer

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

    return context, results

# This function takes a user query, retrieves relevant context from the Qdrant database, and generates an answer using the retrieved context.
def answer_query(query: str):

    context, results = retrieve_context(query)

    answer = generate_answer(
        query=query,
        context=context
    )

    sources = []

    for result in results:
        sources.append({
            "filename": result.payload.get("filename"),
            "page": result.payload.get("page"),
            "chunk_index": result.payload.get("chunk_index"),
            "excerpt": result.payload.get("text")[:200]
        })

    return {
        "answer": answer,
        "sources": sources
    }