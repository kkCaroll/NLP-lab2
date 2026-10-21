import pytest

from recordkit import (
    format_counts,
    format_table,
    group_counts,
    parse_header,
    parse_rows,
    split_fields,
    top_values,
)


def test_split_fields():
    assert split_fields("alice, 30, beijing") == ["alice", "30", "beijing"]
    assert split_fields("single") == ["single"]


def test_split_fields_rejects_non_string():
    with pytest.raises(TypeError):
        split_fields(None)


def test_parse_header():
    assert parse_header("\n name, age, city \nalice,30,beijing\n") == [
        "name",
        "age",
        "city",
    ]
    assert parse_header("") == []


def test_parse_rows():
    text = "name,age,city\nalice,30,beijing\nbob,25,shanghai\n"
    assert parse_rows(text) == [
        {"name": "alice", "age": "30", "city": "beijing"},
        {"name": "bob", "age": "25", "city": "shanghai"},
    ]


def test_parse_rows_fills_missing_fields():
    text = "name,age,city\nalice,30\n"
    assert parse_rows(text) == [{"name": "alice", "age": "30", "city": ""}]


def test_parse_rows_empty_text():
    assert parse_rows("") == []
    assert parse_rows("\n  \n") == []


def test_group_counts_non_string_values():
    records = [{"count": 1}, {"count": 1}, {"count": 2}]
    assert group_counts(records, "count") == {1: 2, 2: 1}


def test_group_counts_empty_and_missing_key():
    assert group_counts([], "city") == {}
    assert group_counts([{"name": "alice"}], "city") == {"": 1}


def test_top_values():
    counts = {"beijing": 3, "shanghai": 2, "shenzhen": 2}
    assert top_values(counts, 2) == [("beijing", 3), ("shanghai", 2)]
    assert top_values(counts, 0) == []


def test_top_values_rejects_bad_limit():
    with pytest.raises(ValueError):
        top_values({}, -1)
    with pytest.raises(TypeError):
        top_values({}, "2")


def test_format_counts():
    assert format_counts({"b": 2, "a": 1}) == "a: 1, b: 2"


def test_format_table():
    records = [{"name": "alice", "age": "30"}]
    assert format_table(records, ["name", "age"]) == "name|age\nalice|30"
    with pytest.raises(ValueError):
        format_table(records, [])
