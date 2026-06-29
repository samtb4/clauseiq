def chunk_text(text: str, chunk_size: int = 1000):
    chunks = []

    for i in range(0, len(text), chunk_size):
        chunk = text[i:i + chunk_size]
        chunks.append(chunk)

    return chunks

# Chunk pages while preserving page numbers.
def chunk_pages(pages, chunk_size: int = 1000):
    chunked_pages = []

    for page in pages:
        page_number = page["page"]
        text = page["text"]

        chunk_index = 0

        for i in range(0, len(text), chunk_size):
            chunked_pages.append({
                "page": page_number,
                "chunk_index": chunk_index,
                "text": text[i:i + chunk_size]
            })

            chunk_index += 1

    return chunked_pages