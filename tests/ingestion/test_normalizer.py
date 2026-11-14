from rag.ingestion.normalizer import TextNormalizer


def test_normalize_whitespace():

    normalizer = TextNormalizer()

    result = normalizer.normalize("Hello     World\n\n\nRAG")

    assert result == "Hello World\n\nRAG"


def test_remove_control_characters():

    normalizer = TextNormalizer()

    result = normalizer.normalize("Hello\x00World")

    assert result == "HelloWorld"
