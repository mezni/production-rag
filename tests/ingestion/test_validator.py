import pytest

from rag.ingestion.validator import (
    DocumentValidationError,
    DocumentValidator,
)


def test_valid_txt_file(tmp_path):

    file_path = tmp_path / "sample.txt"
    file_path.write_text("Hello RAG")

    validator = DocumentValidator()

    validator.validate(file_path)


def test_reject_unsupported_format(tmp_path):

    file_path = tmp_path / "sample.exe"
    file_path.write_text("invalid")

    validator = DocumentValidator()

    with pytest.raises(DocumentValidationError):
        validator.validate(file_path)


def test_reject_empty_file(tmp_path):

    file_path = tmp_path / "empty.txt"
    file_path.write_text("")

    validator = DocumentValidator()

    with pytest.raises(DocumentValidationError):
        validator.validate(file_path)
