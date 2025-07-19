# app/services/pdf_extractor.py
from PyPDF2 import PdfReader
from typing import IO

def extract_text_from_pdf(file: IO[bytes]) -> str:
    """
    Extracts text from an in-memory PDF file.

    Args:
        file: A file-like object representing the PDF.

    Returns:
        The extracted text as a single string.
    """
    try:
        pdf_reader = PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""