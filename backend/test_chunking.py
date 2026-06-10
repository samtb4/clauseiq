from app.services.pdf_service import extract_text_from_pdf
from app.services.chunking_service import chunk_text
# This is a simple test to check if the pdf extraction and chunking is working correctly.
# It will print the total number of chunks and the first 200 characters of the first 3 chunks.
text = extract_text_from_pdf(
    "app/uploads/2024-CS426-Autumn.pdf"
)

chunks = chunk_text(text)

print(f"Total chunks: {len(chunks)}")

for i, chunk in enumerate(chunks[:3]):
    print(f"\nChunk {i + 1}")
    print(chunk[:200])