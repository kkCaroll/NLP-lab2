import pytest

from seqkit.analysis import first_repeat_gap, longest_repeated_run, repeat_gaps
from seqkit.report import duplicate_report
from seqkit.runs import longest_run_value, repeated_runs, run_lengths
from seqkit.search import (
    duplicate_positions,
    find_first_duplicate,
    find_first_in_sorted,
    first_duplicate_index,
    has_duplicate,
)
from seqkit.stats import duplicate_counts, duplicate_ratio, most_common_duplicate


def test_no_duplicates():
    assert find_first_duplicate([1, 2, 3]) is None
    assert first_duplicate_index([1, 2, 3]) is None
    assert has_duplicate([1, 2, 3]) is False


def test_single_duplicate():
    assert find_first_duplicate([1, 2, 3, 2]) == 2
    assert first_duplicate_index([1, 2, 3, 2]) == 1
    assert has_duplicate([1, 2, 3, 2]) is True


def test_duplicate_positions():
    assert duplicate_positions([1, 2, 1, 2, 1]) == {
        1: [0, 2, 4],
        2: [1, 3],
    }


def test_duplicate_counts():
    assert duplicate_counts([1, 2, 1, 2, 1]) == {1: 3, 2: 2}


def test_most_common_duplicate():
    assert most_common_duplicate([1, 2, 1, 2, 1]) == 1
    assert most_common_duplicate([1, 2, 3]) is None


def test_duplicate_ratio():
    assert duplicate_ratio([1, 1, 2, 2, 3]) == 0.8
    assert duplicate_ratio([]) == 0.0


def test_first_repeat_gap():
    assert first_repeat_gap([1, 2, 1, 2]) == 2
    assert first_repeat_gap([1, 2, 2, 1]) == 1
    assert first_repeat_gap([1, 2, 3]) is None


def test_repeat_gaps():
    assert repeat_gaps([1, 2, 1, 2, 1]) == {1: [2, 2], 2: [2]}


def test_longest_repeated_run():
    assert longest_repeated_run([1, 1, 2, 2, 2, 3]) == 3
    assert longest_repeated_run([]) == 0
    assert longest_repeated_run([1, 2, 3]) == 1


def test_find_first_in_sorted():
    assert find_first_in_sorted([3, 4, 5, 5, 5, 5, 6], 5) == 2
    assert find_first_in_sorted([5, 5, 6], 5) == 0
    assert find_first_in_sorted([3, 4, 5], 2) == -1
    assert find_first_in_sorted([3, 4, 5], 6) == -1
    assert find_first_in_sorted([], 1) == -1


def test_run_helpers():
    assert run_lengths([1, 1, 2, 2, 2, 3]) == [2, 3, 1]
    assert repeated_runs([1, 1, 2, 2, 2, 3]) == [(1, 0, 1), (2, 2, 4)]
    assert longest_run_value([1, 1, 2, 2, 2, 3]) == 2
    assert run_lengths([]) == []
    assert repeated_runs([]) == []
    assert longest_run_value([]) is None


def test_empty_sequence():
    assert find_first_duplicate([]) is None
    assert first_duplicate_index([]) is None
    assert has_duplicate([]) is False
    assert duplicate_positions([]) == {}
    assert duplicate_counts([]) == {}
    assert most_common_duplicate([]) is None
    assert first_repeat_gap([]) is None
    assert repeat_gaps([]) == {}
    assert longest_repeated_run([]) == 0
    assert duplicate_ratio([]) == 0.0


def test_invalid_input_type():
    with pytest.raises(TypeError):
        find_first_duplicate("aba")
    with pytest.raises(TypeError):
        find_first_duplicate(123)


def test_unhashable_values_raise():
    with pytest.raises(TypeError):
        find_first_duplicate([[1], [1]])


def test_tuple_input():
    assert find_first_duplicate((1, 2, 1)) == 1


def test_report_single_duplicate():
    report = duplicate_report([1, 2, 3, 2])
    assert report["first_duplicate"] == 2
    assert report["first_index"] == 1
    assert report["has_duplicate"] is True
    assert report["positions"] == {2: [1, 3]}
    assert report["counts"] == {2: 2}
    assert report["most_common"] == 2
    assert report["first_gap"] == 2
    assert report["gaps"] == {2: [2]}
    assert report["longest_run"] == 1
    assert report["ratio"] == 0.5
