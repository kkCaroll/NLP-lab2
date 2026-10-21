import pytest

from slugkit import (
    collapse_blank_lines,
    compare_folded,
    fold_case,
    format_heading,
    format_path,
    format_unique,
    has_accent,
    indent,
    is_slug,
    normalize_title,
    normalize_whitespace,
    shorten_title,
    slug_parts,
    slugify,
    split_words,
    strip_accents,
    title_case,
    title_key,
    unique_slug,
    unique_words,
    word_count,
)


def test_normalize_whitespace():
    assert normalize_whitespace("  a \t b  ") == "a b"
    assert normalize_whitespace("") == ""
    with pytest.raises(TypeError):
        normalize_whitespace(3)


def test_collapse_blank_lines_and_indent():
    assert collapse_blank_lines("a\n\n\nb\n") == "a\n\nb"
    assert indent("a\n\nb", prefix="> ") == "> a\n\n> b"


def test_title_case_and_normalize_title():
    assert title_case("the quick brown fox") == "The Quick Brown Fox"
    assert normalize_title("  the  quick   brown fox ") == "The Quick Brown Fox"
    assert title_key("The Quick Fox") == "the quick fox"


def test_shorten_title():
    assert shorten_title("the quick brown fox", limit=9) == "The Quic…"
    assert shorten_title("short", limit=9) == "Short"
    with pytest.raises(ValueError):
        shorten_title("x", limit=0)


def test_strip_accents_and_helpers():
    assert strip_accents("Café") == "Cafe"
    assert has_accent("Café") is True
    assert has_accent("Cafe") is False
    assert fold_case("CAFÉ") == "cafe"
    assert compare_folded("Café", "CAFE") is True


def test_slugify_simple_text():
    assert slugify(" Hello World ") == "hello-world"
    assert slugify("Café") == "cafe"
    assert slugify("") == ""
    with pytest.raises(TypeError):
        slugify(None)


def test_slug_parts_and_is_slug():
    assert slug_parts("Hello World") == ["hello", "world"]
    assert is_slug("hello-world") is True
    assert is_slug("Hello-World") is False
    assert is_slug("hello--world") is False


def test_unique_slug():
    taken = {"hello-world"}
    assert unique_slug("Hello World", taken) == "hello-world-2"
    taken.add("hello-world-2")
    assert unique_slug("Hello World", taken) == "hello-world-3"
    assert unique_slug("Other Name", taken) == "other-name"


def test_format_path():
    assert format_path(["Hello World", "Q1"]) == "hello-world/q1"
    with pytest.raises(TypeError):
        format_path("Hello")


def test_format_unique():
    assert format_unique(["Hello World", "Hello World", "Other"]) == [
        "hello-world",
        "hello-world-2",
        "other",
    ]


def test_format_heading():
    assert format_heading("the quick brown fox", width=10) == (
        "The Quick Brown Fox\n----------"
    )


def test_split_words_and_counts():
    assert split_words("  a  b ") == ["a", "b"]
    assert split_words("") == []
    assert word_count("a b c") == 3


def test_unique_words():
    assert unique_words("a b A c") == ["a", "b", "c"]
