from app.services.llm_service import generate_answer

answer = generate_answer(
    "What is FastAPI?",
    """
    FastAPI is a modern Python web framework
    used for building APIs.
    """
)

print(answer)