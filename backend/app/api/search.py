from fastapi import APIRouter
from pydantic import BaseModel

# This is the search API endpoint. It takes a user query, retrieves relevant context from the Qdrant database, and returns the context along with the original query.
from app.services.rag_service import retrieve_context

router = APIRouter(
    prefix="/search",
    tags=["Search"]
)


class SearchRequest(BaseModel):
    query: str


@router.post("/")
def search(request: SearchRequest):

    context = retrieve_context(
        request.query
    )

    return {
        "query": request.query,
        "context": context
    }