import fitz

#opens a pdf file and extracts the text from it, returning the text as a string
def extract_text_from_pdf(pdf_path: str) -> str:
    document = fitz.open(pdf_path)

    text = ""

    for page in document:
        text += page.get_text()

    document.close()

    return text