from app.services.pdf_service import extract_text_from_pdf
from app.services.chunking_service import chunk_text
from app.services.embedding_service import create_embedding
from app.services.qdrant_service import (
    create_collection,
    store_chunks
)

create_collection()

text = extract_text_from_pdf(
    "app/uploads/2024-CS426-Autumn.pdf"
)

chunks = chunk_text(text)

embeddings = [
    create_embedding(chunk)
    for chunk in chunks
]

store_chunks(
    chunks,
    embeddings,
    "2024-CS426-Autumn.pdf"
)