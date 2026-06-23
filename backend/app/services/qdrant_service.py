from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from qdrant_client.models import PointStruct
import uuid

# Initialise the Qdrant client to connect to the local Qdrant instance
client = QdrantClient(
    host="localhost",
    port=6333
)

COLLECTION_NAME = "contract_chunks"

# Create a collection in Qdrant if it doesn't already exist
def create_collection():

    collections = client.get_collections()

    existing = [
        c.name
        for c in collections.collections
    ]

    if COLLECTION_NAME not in existing:

        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE
            )
        )

        print("Collection created")

    else:
        print("Collection already exists")

# Store the chunks and their embeddings in the Qdrant collection
def store_chunks(chunks, embeddings, filename):

    points = []

    for chunk, embedding in zip(chunks, embeddings):

        points.append(
            PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding,
                payload={
                    "text": chunk,
                    "filename": filename
                }
            )
        )

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )

    print(f"Stored {len(points)} chunks")

# Search for the most relevant chunks based on the query embedding
def search_chunks(query_embedding, limit=5):

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_embedding,
        limit=limit
    )

    return results.points