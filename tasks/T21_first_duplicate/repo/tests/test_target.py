from seqkit.report import duplicate_report
from seqkit.search import find_first_duplicate, first_duplicate_index


def test_find_first_duplicate_prefers_earliest_value():
    assert find_first_duplicate([3, 1, 3, 2, 1]) == 3


def test_first_duplicate_index_prefers_earliest_value():
    assert first_duplicate_index([3, 1, 3, 2, 1]) == 0


def test_duplicate_report_uses_earliest_value():
    report = duplicate_report([5, 4, 5, 4])
    assert report["first_duplicate"] == 5
    assert report["first_index"] == 0
    assert report["positions"] == {5: [0, 2], 4: [1, 3]}
