from app.services.rag_service import retrieve_context

query = "quaternions"

context = retrieve_context(query)

print(context)