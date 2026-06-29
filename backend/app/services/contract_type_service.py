

import json

from app.services.llm_service import chat_completion

SUPPORTED_CONTRACT_TYPES = [
    "Employment Contract",
    "Service Agreement",
    "Non-Disclosure Agreement",
    "Consulting Agreement",
    "Software Licence Agreement",
    "Lease Agreement",
    "Partnership Agreement",
    "Sales Agreement",
    "Other"
]


def detect_contract_type(text: str):
    """
    Detect the type of contract from the beginning of the document.
    Returns a dictionary containing the contract type and a confidence score.
    """

    prompt = f"""
You are an expert legal document classifier.

Determine the type of contract from the text below.

Choose exactly ONE of these contract types:

{', '.join(SUPPORTED_CONTRACT_TYPES)}

Return ONLY valid JSON in this format:

{{
    "contract_type": "Service Agreement",
    "confidence": 0.97,
    "reason": "Brief explanation of why this document was classified this way."
}}

Document text:
{text[:4000]}
"""

    response = chat_completion(
        prompt,
        json_output=True
    )

    return json.loads(response.choices[0].message.content)