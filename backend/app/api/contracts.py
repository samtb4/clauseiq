from fastapi import APIRouter, UploadFile, File
from pathlib import Path
from app.services.pdf_service import extract_pages_from_pdf
from app.services.chunking_service import chunk_pages
from app.services.embedding_service import create_embedding
from app.services.qdrant_service import create_collection, store_chunks

router = APIRouter(prefix="/contracts", tags=["Contracts"])

UPLOAD_DIR = Path("app/uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@router.post("/upload")
async def upload_contract(file: UploadFile = File(...)):
    
    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)

    pages = extract_pages_from_pdf(str(file_path))
    chunks = chunk_pages(pages)
    

    embeddings = [
        create_embedding(chunk["text"])
        for chunk in chunks
    ]

    create_collection()
    store_chunks(chunks, embeddings, file.filename)

    return {
        "filename": file.filename,
        "status": "uploaded",
        "pages_extracted": len(pages),
        "chunks_created": len(chunks),
        "embeddings_created": len(embeddings)
    }