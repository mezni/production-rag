from pathlib import Path

SUPPORTED_FORMATS = {".pdf", ".docx", ".txt"}


class DocumentValidationError(Exception):
    pass


class DocumentValidator:
    def __init__(self, max_size_mb: int = 20):
        self.max_size_bytes = max_size_mb * 1024 * 1024

    def validate(self, file_path: Path) -> None:

        if not file_path.exists():
            raise DocumentValidationError(f"File does not exist: {file_path}")

        if not file_path.is_file():
            raise DocumentValidationError("Input must be a file")

        if file_path.suffix.lower() not in SUPPORTED_FORMATS:
            raise DocumentValidationError(f"Unsupported format: {file_path.suffix}")

        if file_path.stat().st_size > self.max_size_bytes:
            raise DocumentValidationError("File exceeds maximum allowed size")

        if file_path.stat().st_size == 0:
            raise DocumentValidationError("File is empty")
