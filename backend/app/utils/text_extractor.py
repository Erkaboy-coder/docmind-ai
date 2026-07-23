import re
from pathlib import Path

from docx import Document as DocxDocument
from pypdf import PdfReader

_JUNK_CODEPOINTS = (
    list(range(0, 9))
    + list(range(11, 13))
    + list(range(14, 32))
    + [0xFFFD]
    + list(range(0xE000, 0xF8FF + 1))
)
_JUNK_CHARS = "".join(chr(codepoint) for codepoint in _JUNK_CODEPOINTS)
_JUNK_CHARS_RE = re.compile("[" + re.escape(_JUNK_CHARS) + "]")

# Non-breaking space, zero-width space and other unicode space separators
# that PDF/Office exports leave behind instead of a plain " " -- normalize
# them so they don't confuse chunking or the LLM's reading of the text.
_SPACE_LOOKALIKE_CODEPOINTS = (
    [0xA0, 0x200B, 0x2060] + list(range(0x2000, 0x200A + 1))
)
_SPACE_LOOKALIKE_CHARS = "".join(chr(codepoint) for codepoint in _SPACE_LOOKALIKE_CODEPOINTS)
_SPACE_LOOKALIKE_RE = re.compile("[" + re.escape(_SPACE_LOOKALIKE_CHARS) + "]")

_MULTI_SPACE_RE = re.compile(r"[ \t]+")
_MULTI_BLANK_LINES_RE = re.compile(r"\n{3,}")


def _clean_text(text: str) -> str:
    text = _JUNK_CHARS_RE.sub(" ", text)
    text = _SPACE_LOOKALIKE_RE.sub(" ", text)
    text = _MULTI_SPACE_RE.sub(" ", text)
    text = _MULTI_BLANK_LINES_RE.sub("\n\n", text)
    return text.strip()


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

    return _clean_text(extractor(file_path))
