import pytest

from convertkit import (
    clamp,
    convert_all,
    format_number,
    format_percent,
    format_record,
    is_integer,
    positive_or,
    require_int,
    safe_float,
    safe_int,
)


def test_safe_int_parses_padded_text():
    assert safe_int(" 42 ") == 42
    assert safe_int("-7") == -7
    assert safe_int("+3") == 3


def test_safe_int_returns_default_for_text():
    assert safe_int("abc") == 0
    assert safe_int("", default=11) == 11
    assert safe_int("3.5", default=11) == 11


def test_safe_int_truncates_floats():
    assert safe_int(7.9) == 7
    assert safe_int(-7.9) == -7


def test_safe_float_parses_text():
    assert safe_float(" 2.5 ") == 2.5
    assert safe_float("bad", default=1.5) == 1.5
    assert safe_float(4) == 4.0


def test_convert_all_rejects_non_sequences():
    with pytest.raises(TypeError):
        convert_all("123")


def test_is_integer():
    assert is_integer(3) is True
    assert is_integer(3.0) is True
    assert is_integer(3.5) is False
    assert is_integer(" 8 ") is True
    assert is_integer("8.0") is False
    assert is_integer(True) is False
    assert is_integer(None) is False


def test_require_int():
    assert require_int("12") == 12
    with pytest.raises(ValueError):
        require_int("twelve", name="count")


def test_clamp():
    assert clamp(5, 0, 10) == 5
    assert clamp(-3, 0, 10) == 0
    assert clamp(18, 0, 10) == 10
    with pytest.raises(ValueError):
        clamp(1, 5, 2)


def test_positive_or():
    assert positive_or(4) == 4
    assert positive_or(0) == 0
    assert positive_or("-2") == 0
    assert positive_or(0, fallback=6) == 6


def test_format_number():
    assert format_number("2.345") == "2.35"
    assert format_number("bad", digits=1) == "0.0"
    with pytest.raises(ValueError):
        format_number(1.0, digits=-1)


def test_format_percent():
    assert format_percent(0.256) == "25.6%"
    assert format_percent("0.5", digits=0) == "50%"


def test_format_record():
    assert format_record({"a": 1, "b": "2.5"}) == "a=1.00, b=2.50"
    with pytest.raises(TypeError):
        format_record([1, 2])
