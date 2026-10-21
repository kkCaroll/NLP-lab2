import pytest

from seqkit import (
    compare_sequences,
    count_inversions,
    format_permutations,
    format_sequence,
    is_sorted,
    next_permutation,
    permutations_from,
    rotate_suffix,
    summarize_step,
)


def test_is_sorted():
    assert is_sorted([]) is True
    assert is_sorted([1]) is True
    assert is_sorted([1, 2, 2, 3]) is True
    assert is_sorted([1, 3, 2]) is False


def test_compare_sequences():
    assert compare_sequences([1, 2], [1, 2]) == 0
    assert compare_sequences([1, 2], [1, 3]) == -1
    assert compare_sequences([1, 2, 0], [1, 2]) == 1


def test_count_inversions():
    assert count_inversions([1, 2, 3]) == 0
    assert count_inversions([3, 2, 1]) == 3
    assert count_inversions([]) == 0


def test_next_permutation_returns_none_for_descending_order():
    assert next_permutation([3, 2, 1]) is None


def test_next_permutation_returns_none_for_short_input():
    assert next_permutation([7]) is None
    assert next_permutation([]) is None


def test_next_permutation_does_not_mutate_input():
    values = [3, 2, 1]
    assert next_permutation(values) is None
    assert values == [3, 2, 1]


def test_permutations_from_stops_at_last_order():
    assert permutations_from([3, 2, 1], 2) == []
    assert permutations_from([2, 1], 5) == []


def test_rotate_suffix():
    assert rotate_suffix([1, 2, 3, 4], 2) == [1, 2, 4, 3]
    assert rotate_suffix([1, 2, 3], 0) == [3, 2, 1]
    assert rotate_suffix([1, 2, 3], 3) == [1, 2, 3]


def test_rotate_suffix_rejects_bad_start():
    with pytest.raises(ValueError):
        rotate_suffix([1, 2], 3)
    with pytest.raises(ValueError):
        rotate_suffix([1, 2], -1)


def test_format_sequence():
    assert format_sequence([1, 2, 3]) == "1 -> 2 -> 3"
    assert format_sequence([]) == ""


def test_format_permutations():
    assert format_permutations([[1, 2], [2, 1]]) == ["1 -> 2", "2 -> 1"]


def test_summarize_step():
    assert summarize_step([1, 2, 3], [1, 3, 2]) == "1 -> 2 -> 3 => 1 -> 3 -> 2"
    assert summarize_step([3, 2, 1], None) == "3 -> 2 -> 1; no next permutation"
