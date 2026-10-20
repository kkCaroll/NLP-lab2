from rangekit import parse_many, parse_range


def test_parse_range_includes_upper_bound():
    assert parse_range("1-5") == [1, 2, 3, 4, 5]


def test_parse_many_includes_each_upper_bound():
    assert parse_many(["1-3", "7"]) == [1, 2, 3, 7]
