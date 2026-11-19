from rag.retrieval.query_preprocessor import QueryPreprocessor


def test_preprocess_collapses_whitespace():
    query = "  What is\t the\n refund   policy?  "

    assert QueryPreprocessor.process(query) == "What is the refund policy?"


def test_preprocess_empty_query():
    assert QueryPreprocessor.process("") == ""
