from app.services.pdf_service import extract_text_from_pdf
# This is a simple test to check if the pdf extraction is working correctly. It will print the first 1000 characters of the extracted text from the pdf file.
text = extract_text_from_pdf(
    "app/uploads/2023-CS423-Summer.pdf"
)

print(text[:1000])