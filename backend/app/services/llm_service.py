from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def chat_completion(prompt: str, json_output: bool = False):
    """
    Send a prompt to GPT-4o-mini.

    If json_output=True, the model is instructed to return a valid JSON object.
    """

    request = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    if json_output:
        request["response_format"] = {"type": "json_object"}

    return client.chat.completions.create(**request)


def generate_answer(query: str, context: str):

    prompt = f"""
You are a document analysis assistant.

Answer the user's question using ONLY the provided context.
If the user's query is a keyword or phrase rather than a complete question,
infer the most likely question and answer using the provided context.

If the answer cannot be found in the context, say:
"I could not find that information in the provided document."

Context:
{context}

Question:
{query}
"""

    
    response = chat_completion(prompt)

    return response.choices[0].message.content