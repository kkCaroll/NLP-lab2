from convertkit import convert_all, safe_int


def test_safe_int_uses_the_default_for_missing_values():
    assert safe_int(None, default=-1) == -1


def test_convert_all_replaces_unconvertible_entries():
    assert convert_all([3, None, "7", "abc"]) == [3, 0, 7, 0]
