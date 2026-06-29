

EXPECTED_CLAUSES = {
    "Employment Contract": [
        "Payment Terms",
        "Termination",
        "Confidentiality",
        "Non-Compete",
        "Intellectual Property",
        "Governing Law"
    ],
    "Service Agreement": [
        "Payment Terms",
        "Termination",
        "Liability",
        "Indemnification",
        "Intellectual Property",
        "Governing Law",
        "Dispute Resolution"
    ],
    "Non-Disclosure Agreement": [
        "Confidentiality",
        "Termination",
        "Governing Law",
        "Dispute Resolution"
    ],
    "Consulting Agreement": [
        "Payment Terms",
        "Termination",
        "Confidentiality",
        "Intellectual Property",
        "Liability",
        "Indemnification"
    ],
    "Software Licence Agreement": [
        "Intellectual Property",
        "Payment Terms",
        "Liability",
        "Termination",
        "Governing Law"
    ],
    "Lease Agreement": [
        "Payment Terms",
        "Termination",
        "Liability",
        "Governing Law"
    ],
    "Partnership Agreement": [
        "Payment Terms",
        "Liability",
        "Dispute Resolution",
        "Termination"
    ],
    "Sales Agreement": [
        "Payment Terms",
        "Liability",
        "Termination",
        "Governing Law"
    ]
}


def find_missing_clauses(contract_type: str, detected_clauses: dict):
    """Return the expected clause types that were not detected."""

    expected = EXPECTED_CLAUSES.get(contract_type)

    if not expected:
        return []

    detected = {
        clause["type"]
        for clause in detected_clauses.values()
    }

    return sorted([
        clause
        for clause in expected
        if clause not in detected
    ])