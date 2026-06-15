from app.services.embedding_service import create_embedding

embedding = create_embedding(
    "This contract may be terminated with 30 days notice."
)

print(f"Embedding length: {len(embedding)}")

print(embedding[:10])