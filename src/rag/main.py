from pathlib import Path

from rag.ingestion.service import DocumentIngestionService


def main():

    service = DocumentIngestionService()

    file_path = Path("data/contracts/contract-4821.pdf")

    document = service.ingest(file_path)

    print("Document ID:", document.document_id)
    print("Filename:", document.filename)
    print("File Type:", document.file_type)
    print("Metadata:", document.metadata)

    print("\nExtracted Content:")
    print(document.content)


if __name__ == "__main__":
    main()
