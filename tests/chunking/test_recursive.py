from rag.chunking.recursive import RecursiveCharacterSplitter


def test_empty_text_returns_no_chunks():
    splitter = RecursiveCharacterSplitter(100, 10)

    assert splitter.split("") == []


def test_short_text_returns_one_chunk():
    splitter = RecursiveCharacterSplitter(100, 10)
    text = "This is a short document."

    chunks = splitter.split(text)

    assert len(chunks) == 1
    assert chunks[0][0] == text
    assert chunks[0][1:] == (0, len(text))


def test_long_text_is_split():
    splitter = RecursiveCharacterSplitter(
        chunk_size=100,
        chunk_overlap=10,
    )

    text = "This is a sentence. " * 20

    chunks = splitter.split(text)

    assert len(chunks) > 1
    assert all(len(content) <= 100 for content, _, _ in chunks)


def test_chunks_preserve_original_offsets():
    splitter = RecursiveCharacterSplitter(50, 10)
    text = "First paragraph.\n\nSecond paragraph.\n\nThird paragraph."

    chunks = splitter.split(text)

    for content, start, end in chunks:
        assert text[start:end] == content


def test_chunks_have_overlap():
    splitter = RecursiveCharacterSplitter(50, 10)
    text = "A " * 100

    chunks = splitter.split(text)

    assert len(chunks) > 1

    first_end = chunks[0][2]
    second_start = chunks[1][1]

    assert second_start < first_end
