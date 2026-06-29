from fastapi import APIRouter, UploadFile, File
from pathlib import Path
from app.services.pdf_service import extract_pages_from_pdf
from app.services.chunking_service import chunk_pages
from app.services.embedding_service import create_embedding
from app.services.qdrant_service import create_collection, store_chunks

from app.services.qdrant_service import client, COLLECTION_NAME
from app.services.clause_service import classify_clause
from app.services.contract_type_service import detect_contract_type
from app.services.missing_clause_service import find_missing_clauses

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


# New endpoint: analyse_contract
@router.post("/analyse")
def analyse_contract():

    results = client.scroll(
        collection_name=COLLECTION_NAME,
        limit=1000,
        with_payload=True,
        with_vectors=False
    )[0]

    if not results:
        return {
            "filename": None,
            "contract_type": None,
            "contract_type_confidence": 0,
            "overall_risk": "Unknown",
            "risk_score": 0,
            "missing_clauses": [],
            "total_clauses": 0,
            "clauses": []
        }

    combined_text = "\n\n".join(
        result.payload["text"]
        for result in results[:5]
    )

    contract_info = detect_contract_type(combined_text)

    detected_clauses = {}

    for result in results:
        payload = result.payload

        classification = classify_clause(payload["text"])
        clause_type = classification.get("type")

        if not clause_type:
            continue

        if clause_type not in detected_clauses:
            detected_clauses[clause_type] = {
                "type": clause_type,
                "summary": classification.get("summary"),
                "confidence": classification.get("confidence"),
                "filename": payload.get("filename"),
                "risk": classification.get("risk"),
                "reason": classification.get("reason"),
                "pages": [payload.get("page")]
            }
        else:
            page = payload.get("page")
            if page not in detected_clauses[clause_type]["pages"]:
                detected_clauses[clause_type]["pages"].append(page)

    # Sort page numbers for each detected clause.
    for clause in detected_clauses.values():
        clause["pages"].sort()

    risk_values = {
        "Low": 1,
        "Medium": 2,
        "High": 3
    }

    if detected_clauses:
        average_risk = sum(
            risk_values.get(clause["risk"], 2)
            for clause in detected_clauses.values()
        ) / len(detected_clauses)

        if average_risk < 1.5:
            overall_risk = "Low"
        elif average_risk < 2.5:
            overall_risk = "Medium"
        else:
            overall_risk = "High"

        risk_score = round((average_risk / 3) * 100)

        filename = next(iter(detected_clauses.values()))["filename"]
    else:
        overall_risk = "Unknown"
        risk_score = 0
        filename = None

    missing_clauses = find_missing_clauses(
        contract_info.get("contract_type"),
        detected_clauses
    )

    return {
        "filename": filename,
        "contract_type": contract_info.get("contract_type"),
        "contract_type_confidence": contract_info.get("confidence"),
        "contract_type_reason": contract_info.get("reason"),
        "overall_risk": overall_risk,
        "risk_score": risk_score,
        "missing_clauses": missing_clauses,
        "total_clauses": len(detected_clauses),
        "clauses": list(detected_clauses.values())
    }