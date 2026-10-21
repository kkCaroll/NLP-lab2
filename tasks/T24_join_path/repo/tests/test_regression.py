import pytest

from pathmont import (
    append_name,
    as_posix,
    base_name,
    check_parts,
    clean_path,
    common_root,
    describe_path,
    extension,
    format_count,
    format_ext,
    format_relative,
    format_tree,
    has_extension,
    is_absolute_style,
    is_clean,
    is_within,
    join_many,
    join_path,
    join_url,
    relative_to_root,
    resolve_under,
    safe_segment,
    sanitize_segment,
    segment_depth,
    split_ext,
    split_parts,
    stem,
    with_suffix,
)


def test_clean_path():
    assert clean_path("./data//reports/") == "data/reports"
    assert clean_path("") == "."
    assert as_posix("data\\reports") == "data/reports"
    assert is_clean("data/reports") is True
    assert is_clean("data//reports") is False


def test_path_parts():
    assert split_parts("./data//reports/") == ["data", "reports"]
    assert split_parts("") == []
    assert is_absolute_style("/data") is True
    assert is_absolute_style("data") is False


def test_join_relative_parts():
    assert join_path("data", "reports", "q1.csv") == "data/reports/q1.csv"
    assert join_path("data", "reports/") == "data/reports/"
    assert join_many("data", ["a", "b"]) == "data/a/b"
    assert append_name("data", "file.txt") == "data/file.txt"


def test_join_url():
    assert join_url("https://example.test/", "a", "/b") == "https://example.test/a/b"
    assert join_url("https://example.test") == "https://example.test"


def test_resolve_and_relative():
    assert resolve_under("data", "reports", "q1.csv") == "data/reports/q1.csv"
    assert is_within("data", "data/reports/q1.csv") is True
    assert is_within("data", "other/q1.csv") is False
    assert relative_to_root("data", "data/reports/q1.csv") == "reports/q1.csv"
    assert relative_to_root("data", "data") == "."
    with pytest.raises(ValueError):
        relative_to_root("data", "other/q1.csv")


def test_common_root():
    assert common_root(["data/a/x", "data/a/y"]) == "data/a"
    assert common_root(["data/a", "other/b"]) == "."


def test_extension_helpers():
    assert split_ext("data/report.tar.gz") == ("data/report.tar", ".gz")
    assert base_name("data/report.txt") == "report.txt"
    assert stem("data/report.txt") == "data/report"
    assert extension("data/report.txt") == ".txt"
    assert with_suffix("data/report.txt", ".csv") == "data/report.csv"
    assert has_extension("data/report.TXT", ".txt") is True
    with pytest.raises(ValueError):
        with_suffix("data/report.txt", "csv")


def test_segment_helpers():
    assert safe_segment("report") == "report"
    assert check_parts(["a", "b"]) == ["a", "b"]
    assert sanitize_segment("a b") == "a_b"
    assert sanitize_segment("") == "_"
    assert segment_depth("data/reports/q1.csv") == 3
    with pytest.raises(ValueError):
        safe_segment("..")
    with pytest.raises(ValueError):
        safe_segment("../etc")


def test_report_helpers():
    assert describe_path("data/a") == "data/a (relative)"
    assert describe_path("/data/a") == "/data/a (absolute)"
    assert format_tree(["data/b", "data/a"]) == "  data/a\n  data/b"
    assert format_relative("data", ["data/a"]) == "a"
    assert format_ext("data/a.txt") == ".txt"
    assert format_ext("data/a") == "-"
    assert format_count(["a", "b"]) == "paths=2"
