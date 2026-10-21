import pytest

from rankkit import (
    format_ranking,
    format_table,
    mean,
    median,
    rank_of,
    sorted_descending,
    spread,
    summarize,
    top_k,
)


def test_sorted_descending_returns_a_copy():
    values = [2, 7, 4]
    assert sorted_descending(values) == [7, 4, 2]
    assert values == [2, 7, 4]


def test_sorted_descending_rejects_non_sequences():
    with pytest.raises(TypeError):
        sorted_descending(42)


def test_top_k_on_an_empty_list():
    assert top_k([], 0) == []


def test_top_k_with_a_full_limit():
    assert top_k([4, 1, 3], 3) == [4, 3, 1]


def test_top_k_rejects_bad_limits():
    with pytest.raises(ValueError):
        top_k([1, 2], -1)
    with pytest.raises(TypeError):
        top_k([1, 2], "1")


def test_mean():
    assert mean([2, 4, 6]) == 4
    with pytest.raises(ValueError):
        mean([])


def test_median():
    assert median([5, 1, 3]) == 3
    assert median([4, 1, 3, 2]) == 2.5
    with pytest.raises(TypeError):
        median(3)


def test_spread():
    assert spread([4, 9, 2]) == 7
    with pytest.raises(ValueError):
        spread([])


def test_rank_of():
    assert rank_of(9, [9, 5, 7]) == 1
    assert rank_of(6, [9, 5, 7]) == 3
    assert rank_of(1, [9, 5, 7]) == 4


def test_format_ranking():
    assert format_ranking([("ana", 9), ("bo", 7)]) == "1. ana: 9\n2. bo: 7"


def test_format_table():
    assert format_table([("ana", 9)], width=5) == "name  score\nana   9"


def test_summarize():
    assert summarize([2, 4, 6]) == "count=3 mean=4.00 spread=4"
