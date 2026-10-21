from textscan import extract_versions


def test_extract_versions_rejects_a_numeric_suffix():
    assert extract_versions("build 1.2.3.4") == []


def test_extract_versions_keeps_only_complete_versions():
    assert extract_versions("1.2.3.4 and 5.6.7") == ["5.6.7"]
