from datetime import date, datetime

import pytest

from timekit import (
    days_between,
    format_compact,
    format_time,
    is_weekend,
    month_length,
    next_weekday,
    parse_date,
    parse_datetime,
    parse_many,
    parse_optional,
)


def test_format_time():
    assert format_time(datetime(2024, 3, 5, 14, 7)) == "14:07"
    assert format_time(datetime(2024, 12, 1, 0, 0)) == "00:00"
    with pytest.raises(TypeError):
        format_time(date(2024, 3, 5))


def test_format_compact():
    assert format_compact(datetime(2024, 3, 5)) == "20240305"
    assert format_compact(date(1999, 12, 31)) == "19991231"


def test_parse_date():
    assert parse_date(" 2024-03-05 ") == date(2024, 3, 5)
    with pytest.raises(ValueError):
        parse_date("05/03/2024")
    with pytest.raises(TypeError):
        parse_date(20240305)


def test_parse_datetime():
    assert parse_datetime("2024-11-23 14:07") == datetime(2024, 11, 23, 14, 7)
    with pytest.raises(ValueError):
        parse_datetime("2024-11-23")


def test_parse_optional():
    assert parse_optional("") is None
    assert parse_optional(None) is None
    assert parse_optional("2024-03-05") == date(2024, 3, 5)
    assert parse_optional("2024-03-05 08:30") == datetime(2024, 3, 5, 8, 30)


def test_parse_many():
    assert parse_many(["2024-03-05", "", "2024-03-06"]) == [
        date(2024, 3, 5),
        date(2024, 3, 6),
    ]
    with pytest.raises(TypeError):
        parse_many("2024-03-05")


def test_days_between():
    assert days_between(date(2024, 3, 1), date(2024, 3, 5)) == 4
    assert days_between(date(2024, 3, 5), date(2024, 3, 1)) == -4
    with pytest.raises(TypeError):
        days_between("2024-03-01", date(2024, 3, 5))


def test_is_weekend():
    assert is_weekend(date(2024, 3, 2)) is True
    assert is_weekend(date(2024, 3, 3)) is True
    assert is_weekend(date(2024, 3, 4)) is False


def test_next_weekday():
    assert next_weekday(date(2024, 3, 1)) == date(2024, 3, 4)
    assert next_weekday(date(2024, 3, 5)) == date(2024, 3, 6)


def test_month_length():
    assert month_length(date(2024, 2, 10)) == 29
    assert month_length(date(2023, 2, 10)) == 28
    assert month_length(date(2024, 12, 1)) == 31
