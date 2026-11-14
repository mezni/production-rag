from pathlib import Path
from typing import Protocol

from docx import Document as WordDocument
from pypdf import PdfReader


class DocumentParser(Protocol):

    def parse(self, file_path: Path) -> str:
        ...


class PDFParser:

    def parse(self, file_path: Path) -> str:
        reader = PdfReader(str(file_path))

        pages = []

        for page in reader.pages:
            text = page.extract_text() or ""
            pages.append(text)

        return "\n".join(pages)


class DOCXParser:

    def parse(self, file_path: Path) -> str:
        document = WordDocument(file_path)

        paragraphs = [
            paragraph.text
            for paragraph in document.paragraphs
        ]

        return "\n".join(paragraphs)


class TXTParser:

    def parse(self, file_path: Path) -> str:
        return file_path.read_text(
            encoding="utf-8",
            errors="replace",
        )


class ParserFactory:

    @staticmethod
    def create(file_path: Path) -> DocumentParser:

        extension = file_path.suffix.lower()

        parsers = {
            ".pdf": PDFParser,
            ".docx": DOCXParser,
            ".txt": TXTParser,
        }

        parser_class = parsers.get(extension)

        if parser_class is None:
            raise ValueError(
                f"No parser available for {extension}"
            )

        return parser_class()
