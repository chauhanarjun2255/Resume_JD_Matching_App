import pdfplumber
import docx
from io import BytesIO


def extract_pdf(file):
    """Extract text from PDF."""
    text = ""

    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    if not text.strip():
        return "No readable text found in PDF."

    return text


def extract_docx(file):
    """Extract text from DOCX."""
    document = docx.Document(BytesIO(file.read()))

    text = ""

    for paragraph in document.paragraphs:
        text += paragraph.text + "\n"

    return text


def extract_txt(file):
    """Extract text from TXT."""
    return file.read().decode("utf-8")


def extract_resume(file):
    """
    Detect file type automatically
    """
    try:
        filename = file.name.lower()

        if filename.endswith(".pdf"):
            return extract_pdf(file)

        elif filename.endswith(".docx"):
            return extract_docx(file)

        elif filename.endswith(".txt"):
            return extract_txt(file)

        else:
            return "Unsupported File Format"

    except Exception as e:
        return f"Error: {str(e)}"