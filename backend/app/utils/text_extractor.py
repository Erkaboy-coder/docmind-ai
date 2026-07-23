from pathlib import Path

from docx import Document as DocxDocument
from pypdf import PdfReader


def extract_pdf_text(file_path: Path) -> str:
    reader = PdfReader(file_path)

    pages = [page.extract_text() or "" for page in reader.pages]

    return "\n".join(pages).strip()


def extract_docx_text(file_path: Path) -> str:
    document = DocxDocument(file_path)

    paragraphs = [p.text for p in document.paragraphs]

    return "\n".join(paragraphs).strip()


def extract_txt_text(file_path: Path) -> str:
    return file_path.read_text(encoding="utf-8", errors="ignore").strip()


EXTRACTORS = {
    "pdf": extract_pdf_text,
    "docx": extract_docx_text,
    "txt": extract_txt_text,
}


def extract_text(file_path: Path, file_type: str) -> str:
    extractor = EXTRACTORS.get(file_type)

    if extractor is None:
        raise ValueError(f"Unsupported file type: {file_type}")

    return extractor(file_path)
