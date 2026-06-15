from sentence_transformers import SentenceTransformer
# This service is responsible for creating embeddings for the text using the SentenceTransformer model. 
# The model used is "all-MiniLM-L6-v2", which is a lightweight and efficient model for generating sentence embeddings.
model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

def create_embedding(text: str):
    return model.encode(text).tolist()