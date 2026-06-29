import json

from app.services.llm_service import chat_completion

CLAUSE_TYPES = [
    "Termination",
    "Confidentiality",
    "Liability",
    "Payment Terms",
    "Intellectual Property",
    "Governing Law",
    "Force Majeure",
    "Indemnification",
    "Non-Compete",
    "Dispute Resolution"
]


def classify_clause(chunk: str):
    """
    Analyse a single chunk of text and determine whether it contains
    one of the supported legal clause types.
    """

    prompt = f"""
You are an expert legal contract analysis assistant.

Determine whether the supplied text contains one of the following clause types:

{', '.join(CLAUSE_TYPES)}

Return ONLY valid JSON.

If a clause is found, return ONLY valid JSON in this format:
{{
    "type": "Termination",
    "summary": "Brief summary of the clause.",
    "confidence": 0.95,
    "risk": "Low",
    "reason": "Explain why this clause has this level of risk in one or two sentences."
}}

Risk must be exactly one of:
- Low
- Medium
- High

Assess both the legal and commercial risk of the clause when choosing the risk level.

If no clause matches:
{{
    "type": null
}}

Text:
{chunk}
"""

    response = chat_completion(
        prompt,
        json_output=True
    )

    return json.loads(response.choices[0].message.content)