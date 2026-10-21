import pytest

from listkit import (
    chunk,
    deduplicate,
    flatten,
    format_items,
    format_records,
    format_sorted,
    partition,
    rotate,
    sort_by_key,
    sort_items,
)


def test_sort_items_rejects_non_sequences():
    with pytest.raises(TypeError):
        sort_items(7)


def test_sort_by_key():
    records = [
        {"name": "ana", "score": 7},
        {"name": "bo", "score": 9},
        {"name": "cy", "score": 8},
    ]
    assert [record["name"] for record in sort_by_key(records, "score")] == [
        "ana",
        "cy",
        "bo",
    ]
    assert [record["name"] for record in sort_by_key(records, "score", reverse=True)] == [
        "bo",
        "cy",
        "ana",
    ]


def test_sort_by_key_errors():
    with pytest.raises(KeyError):
        sort_by_key([{"name": "ana"}], "score")
    with pytest.raises(TypeError):
        sort_by_key([], 3)


def test_deduplicate():
    assert deduplicate([3, 1, 3, 2, 1]) == [3, 1, 2]
    assert deduplicate([]) == []


def test_partition():
    matches, rest = partition([1, 2, 3, 4], lambda value: value % 2 == 0)
    assert matches == [2, 4]
    assert rest == [1, 3]
    with pytest.raises(TypeError):
        partition([1], "even")


def test_flatten():
    assert flatten([[1, 2], (3,), []]) == [1, 2, 3]
    with pytest.raises(TypeError):
        flatten([[1], 2])


def test_chunk():
    assert chunk([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]]
    assert chunk([], 3) == []
    with pytest.raises(ValueError):
        chunk([1], 0)


def test_rotate():
    assert rotate([1, 2, 3], 1) == [2, 3, 1]
    assert rotate([1, 2, 3], -1) == [3, 1, 2]
    assert rotate([], 2) == []


def test_format_items():
    assert format_items([1, 2, 3], separator="-") == "1-2-3"
    with pytest.raises(TypeError):
        format_items([1], separator=3)


def test_format_records():
    records = [{"name": "ana", "score": 9}, {"name": "bo"}]
    assert format_records(records, ["name", "score"]) == "ana | 9\nbo | "


def test_format_sorted():
    assert format_sorted((3, 1, 2)) == "1, 2, 3"
