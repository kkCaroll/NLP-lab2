from datetime import datetime

from timekit import format_date, format_datetime


def test_format_date_renders_the_month_field():
    assert format_date(datetime(2024, 3, 5)) == "2024-03-05"


def test_format_datetime_renders_month_and_minute():
    assert format_datetime(datetime(2024, 11, 23, 14, 7)) == "2024-11-23 14:07"
