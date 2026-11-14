from pathlib import Path


class MetadataExtractor:
    def extract(self, file_path: Path) -> dict:

        return {
            "source_path": str(file_path.resolve()),
            "document_type": self._get_document_type(file_path),
            "extension": file_path.suffix.lower(),
            "file_size_bytes": file_path.stat().st_size,
        }

    def _get_document_type(self, file_path: Path) -> str:

        name = file_path.stem.lower()

        if "contract" in name:
            return "contract"

        if "policy" in name:
            return "policy"

        if "procedure" in name:
            return "procedure"

        return "unknown"
