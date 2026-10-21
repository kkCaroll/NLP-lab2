import pytest

from recordkit import (
    department_lines,
    department_summary,
    format_names,
    format_table,
    group_by_department,
    normalize_name,
    normalize_record,
    normalize_records,
    parse_age,
    rank_records,
    sort_records,
    summary,
    top_k,
)

ROSTER = [
    {"id": "e1", "name": "Cara", "age": 25, "department": "research"},
    {"id": "e2", "name": "bob", "age": 30, "department": "research"},
    {"id": "e3", "name": "Ana", "age": 30, "department": "operations"},
    {"id": "e4", "name": "dave", "age": 41, "department": "operations"},
]


def test_parse_age_accepts_integers_and_digit_strings():
    assert parse_age(30) == 30
    assert parse_age("042") == 42
    assert parse_age(" 7 ") == 7


def test_parse_age_rejects_bool_negative_and_noise():
    with pytest.raises(TypeError):
        parse_age(True)
    for value in (-1, "x", 3.5, None):
        with pytest.raises(ValueError):
            parse_age(value)


def test_normalize_name_collapses_whitespace():
    assert normalize_name("  Ana   Maria ") == "Ana Maria"
    assert normalize_name("bob") == "bob"


def test_normalize_name_rejects_empty_and_non_text():
    with pytest.raises(TypeError):
        normalize_name(30)
    for value in ("", "   "):
        with pytest.raises(ValueError):
            normalize_name(value)


def test_normalize_record_normalizes_fields():
    record = {
        "id": " e1 ",
        "name": "  Ana   Maria ",
        "age": "30",
        "department": " research ",
    }
    assert normalize_record(record) == {
        "id": "e1",
        "name": "Ana Maria",
        "age": 30,
        "department": "research",
    }
    assert record["name"] == "  Ana   Maria "


def test_normalize_record_requires_every_field():
    with pytest.raises(KeyError):
        normalize_record({"id": "e1", "name": "Ana", "age": 30})
    with pytest.raises(TypeError):
        normalize_record(["e1", "Ana", 30, "research"])


def test_normalize_records_rejects_non_sequence():
    for value in ({}, "abc", 30):
        with pytest.raises(TypeError):
            normalize_records(value)
    assert normalize_records([]) == []


def test_sort_records_returns_new_list_without_mutating_input():
    original = [dict(record) for record in ROSTER]
    result = sort_records(ROSTER)
    assert ROSTER == original
    assert result is not ROSTER
    assert all(isinstance(record["age"], int) for record in result)


def test_sort_records_handles_empty_and_single_record():
    assert sort_records([]) == []
    single = sort_records([ROSTER[0]])
    assert len(single) == 1
    assert single[0]["name"] == "Cara"


def test_sort_records_is_stable_and_ranks_identical_keys():
    records = [
        {"id": "e1", "name": "Ana", "age": 30, "department": "ops"},
        {"id": "e2", "name": "Ana", "age": 30, "department": "ops"},
        {"id": "e3", "name": "Ana", "age": 30, "department": "ops"},
    ]
    assert [record["id"] for record in sort_records(records)] == ["e1", "e2", "e3"]
    assert [row["rank"] for row in rank_records(records)] == [1, 1, 1]


def test_top_k_validates_k_and_handles_empty_result():
    assert top_k(ROSTER, 0) == []
    assert top_k(ROSTER, -2) == []
    assert len(top_k(ROSTER, 10)) == 4
    for value in (True, "2", 2.5):
        with pytest.raises(TypeError):
            top_k(ROSTER, value)


def test_group_by_department_preserves_input_order():
    groups = group_by_department(ROSTER)
    assert list(groups) == ["research", "operations"]
    assert [record["name"] for record in groups["research"]] == ["Cara", "bob"]
    assert [record["name"] for record in groups["operations"]] == ["Ana", "dave"]


def test_department_summary_reports_count_average_and_names():
    rows = department_summary(ROSTER)
    assert [row["department"] for row in rows] == ["operations", "research"]
    assert rows[1]["count"] == 2
    assert rows[1]["average_age"] == 27.5
    assert rows[1]["names"] == ["Cara", "bob"]
    assert rows[0]["average_age"] == 35.5


def test_summary_and_table_handle_extremes_and_single_row():
    result = summary(ROSTER)
    assert result["count"] == 4
    assert result["oldest"] == "dave"
    assert result["youngest"] == "Cara"
    assert result["average_age"] == 31.5
    assert summary([]) == {
        "count": 0,
        "oldest": None,
        "youngest": None,
        "average_age": 0,
    }
    assert format_table([]) == "name\tage\tdepartment"
    assert format_table([ROSTER[0]]) == "name\tage\tdepartment\nCara\t25\tresearch"
    assert format_names([ROSTER[0]]) == "Cara"
    assert department_lines(ROSTER) == [
        "operations: 2 people, average 35.5",
        "research: 2 people, average 27.5",
    ]
