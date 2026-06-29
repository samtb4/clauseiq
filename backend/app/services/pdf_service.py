import fitz

#opens a pdf file and extracts the text from it, returning the text as a string
def extract_text_from_pdf(pdf_path: str) -> str:
    document = fitz.open(pdf_path)

    text = ""

    for page in document:
        text += page.get_text()

    document.close()

    return text

# Extract text page-by-page while preserving page numbers.
def extract_pages_from_pdf(pdf_path: str):
    document = fitz.open(pdf_path)

    pages = []

    for page_number, page in enumerate(document, start=1):
        pages.append({
            "page": page_number,
            "text": page.get_text()
        })

    document.close()

    return pages