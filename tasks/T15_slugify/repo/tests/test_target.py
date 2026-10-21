from slugkit import format_index, slugify


def test_slugify_collapses_punctuation_runs():
    assert slugify("Hello, World!") == "hello-world"


def test_format_index_collapses_separators():
    assert format_index([("Data -- Science", 3)]) == "data-science: 3"
