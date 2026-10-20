import pytest

from rangekit import (
    expand_ranges,
    format_ranges,
    merge_ranges,
    parse_many,
    parse_range,
    summarize,
    unique_values,
    validate_range,
)


def test_parse_single_value():
    assert parse_range("4") == [4]
    assert parse_range(" 7 ") == [7]


def test_parse_range_rejects_reversed_bounds():
    with pytest.raises(ValueError):
        parse_range("5-1")


def test_parse_range_rejects_non_numeric_text():
    with pytest.raises(ValueError):
        parse_range("a-b")
    with pytest.raises(ValueError):
        parse_range("")


def test_parse_range_rejects_non_string_input():
    with pytest.raises(TypeError):
        parse_range(5)


def test_parse_many_flattens_single_values():
    assert parse_many(["1", "3", "5"]) == [1, 3, 5]
    assert parse_many(("2", "4")) == [2, 4]


def test_parse_many_rejects_non_list_input():
    with pytest.raises(TypeError):
        parse_many("1-2")
    with pytest.raises(TypeError):
        parse_many(None)


def test_merge_ranges_overlapping():
    assert merge_ranges([(1, 3), (2, 5), (8, 9)]) == [(1, 5), (8, 9)]
    assert merge_ranges([]) == []


def test_merge_ranges_adjacent():
    assert merge_ranges([(1, 2), (3, 4)]) == [(1, 4)]
    assert merge_ranges([(5, 6), (1, 2)]) == [(1, 2), (5, 6)]


def test_format_ranges():
    assert format_ranges([(1, 3), (5, 5)]) == ["1-3", "5"]


def test_summarize_ranges():
    assert summarize([(1, 3), (5, 5)]) == "1-3, 5"


def test_unique_values_keep_first_seen_order():
    assert unique_values([3, 1, 3, 2, 1]) == [3, 1, 2]


def test_expand_ranges():
    assert expand_ranges([(1, 3), (5, 5)]) == [1, 2, 3, 5]


def test_validate_range_rejects_invalid_pairs():
    with pytest.raises(ValueError):
        validate_range(4, 2)
    with pytest.raises(TypeError):
        validate_range(1, True)
