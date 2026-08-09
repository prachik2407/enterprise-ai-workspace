from pathlib import Path

from pypdf import PdfReader

from app.ai.parsers.base import BaseParser


class PDFParser(BaseParser):
    """Parser for PDF documents."""

    def parse(self, file_path: Path) -> str:
        """Extract text from all pages of a PDF."""

        reader = PdfReader(str(file_path))

        text_parts: list[str] = []

        for page in reader.pages:
            text = page.extract_text()

            if text:
                text_parts.append(text)

        return "\n".join(text_parts)