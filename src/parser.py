"""Privacy-conscious text extraction from common resume file formats."""
from pathlib import Path
from io import BytesIO

def extract_text_from_bytes(filename: str, content: bytes) -> str:
    """Extract text from a PDF, DOCX or TXT upload without persisting the file."""
    suffix = Path(filename).suffix.lower()
    if suffix == ".txt":
        return content.decode("utf-8", errors="replace")
    if suffix == ".pdf":
        from pypdf import PdfReader
        reader = PdfReader(BytesIO(content))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    if suffix == ".docx":
        from docx import Document
        document = Document(BytesIO(content))
        return "\n".join(paragraph.text for paragraph in document.paragraphs)
    raise ValueError("Unsupported file type. Upload a PDF, DOCX or TXT resume.")
