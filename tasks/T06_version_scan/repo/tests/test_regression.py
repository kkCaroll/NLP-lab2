import pytest

from textscan import (
    collapse_blank_lines,
    extract_versions,
    find_version_positions,
    format_versions,
    group_by_major,
    has_prerelease,
    is_version,
    normalize_spaces,
    replace_versions,
    strip_punctuation,
    summarize_versions,
    trim_lines,
    version_majors,
)


def test_extract_versions_normal_forms():
    assert extract_versions("v1.2.3 and 2.0.0-beta") == ["1.2.3", "2.0.0-beta"]
    assert extract_versions("nothing here") == []


def test_extract_versions_rejects_non_string():
    with pytest.raises(TypeError):
        extract_versions(None)


def test_is_version():
    assert is_version("v1.2.3") is True
    assert is_version("2.0.0-beta") is True
    assert is_version("1.2") is False
    assert is_version("1.2.3.4") is False


def test_replace_versions():
    assert replace_versions("upgrade 1.2.3 now", "X") == "upgrade X now"
    assert replace_versions("v2.0.0-beta ready", "release") == "release ready"
    with pytest.raises(TypeError):
        replace_versions("1.2.3", None)


def test_normalize_spaces():
    assert normalize_spaces("  alpha \t beta \n gamma ") == "alpha beta gamma"


def test_line_normalisation():
    assert trim_lines(" a \n b  \n") == "a\nb"
    assert collapse_blank_lines("a\n\n  \nb\n") == "a\nb"


def test_strip_punctuation():
    assert strip_punctuation("...hello, world!?") == "hello, world"
    assert strip_punctuation("no punctuation") == "no punctuation"


def test_version_majors():
    assert version_majors(["1.2.3", "10.20.30", "1.5.0"]) == [1, 10, 1]


def test_group_by_major():
    assert group_by_major(["1.2.3", "2.0.0", "1.5.0"]) == {
        1: ["1.2.3", "1.5.0"],
        2: ["2.0.0"],
    }


def test_summarize_versions():
    assert summarize_versions([]) == {"count": 0, "majors": {}}
    assert summarize_versions(["1.2.3", "1.4.0", "2.0.0"]) == {
        "count": 3,
        "majors": {1: 2, 2: 1},
    }


def test_format_versions():
    assert format_versions(["1.2.3", "2.0.0"]) == "1.2.3, 2.0.0"


def test_find_version_positions():
    text = "v1.2.3 then 2.0.0-beta"
    positions = find_version_positions(text)
    assert [item[2] for item in positions] == ["1.2.3", "2.0.0-beta"]
    assert text[positions[0][0]:positions[0][1]] == "1.2.3"


def test_has_prerelease():
    assert has_prerelease("2.0.0-beta") is True
    assert has_prerelease("2.0.0") is False
