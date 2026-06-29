from fastapi import APIRouter
from pydantic import BaseModel

# Search API endpoint. Accepts a user query, performs RAG retrieval and answer generation, and returns the generated answer together with its supporting sources.
from app.services.rag_service import answer_query

router = APIRouter(
    prefix="/search",
    tags=["Search"]
)


class SearchRequest(BaseModel):
    query: str


@router.post("/")
def search(request: SearchRequest):

    result = answer_query(request.query)

    return {
        "query": request.query,
        "answer": result["answer"],
        "sources": result["sources"]
    }