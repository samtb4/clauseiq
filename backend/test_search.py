from app.services.embedding_service import create_embedding
from app.services.qdrant_service import search_chunks

query = "What are the exam questions?"

query_embedding = create_embedding(query)

results = search_chunks(query_embedding)

for i, result in enumerate(results):

    print(f"\nResult {i+1}")
    print(result.payload["text"][:300])