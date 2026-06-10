from fastapi import APIRouter, UploadFile, File
from pathlib import Path
from app.services.pdf_service import extract_text_from_pdf

router = APIRouter(prefix="/contracts", tags=["Contracts"])

UPLOAD_DIR = Path("app/uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@router.post("/upload")
async def upload_contract(file: UploadFile = File(...)):
    
    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)

    text = extract_text_from_pdf(str(file_path))

    return {
        "filename": file.filename,
        "status": "uploaded",
        "characters_extracted": len(text)
    }