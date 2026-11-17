from pathlib import Path

from rag.ingestion.metadata import MetadataExtractor
from rag.ingestion.normalizer import TextNormalizer
from rag.ingestion.parser import ParserFactory
from rag.ingestion.validator import DocumentValidator
from rag.models.document import Document


class DocumentIngestionService:
    def __init__(self):

        self.validator = DocumentValidator()
        self.normalizer = TextNormalizer()
        self.metadata_extractor = MetadataExtractor()

    def ingest(self, file_path: Path) -> Document:

        # 1. Validate
        self.validator.validate(file_path)

        # 2. Select parser
        parser = ParserFactory.create(file_path)

        # 3. Extract content
        raw_content = parser.parse(file_path)

        if not raw_content.strip():
            raise ValueError(f"No text extracted from {file_path.name}")

        # 4. Normalize
        content = self.normalizer.normalize(raw_content)

        # 5. Extract metadata
        metadata = self.metadata_extractor.extract(file_path)

        # 6. Build standard document
        return Document(
            document_id=file_path.stem,
            filename=file_path.name,
            file_type=file_path.suffix.lower().lstrip("."),
            content=content,
            metadata=metadata,
        )
