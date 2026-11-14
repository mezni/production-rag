# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Document ingestion service with validation, parsing, normalization, and
  metadata extraction.
- PDF, DOCX, and TXT parsers behind a `ParserFactory`.
- Text normalizer and standard `Document` domain model.
- Sample documents under `data/` for contracts, policies, and procedures.
- Runtime dependencies: `python-docx` and `pypdf`.

### Changed

- `.gitignore` now covers Python caches, virtual environments, build artifacts,
  environment files, and editor/OS files.

### Removed

- `__pycache__` directories and their compiled `.pyc` files from version control.

## [0.1.0] - 2026-11-13

### Added

- Initial document ingestion project scaffold.
- Standard document domain model.
- Document file validation.
- PDF, DOCX, and TXT parsers.
- Text normalization.
- Document ingestion service.
- Document ingestion unit tests.
