"""Calendar interval helpers."""

from datetime import date, timedelta


def _require_date(moment):
    if not isinstance(moment, date):
        raise TypeError("moment must be a date")


def days_between(start, end):
    """Return the number of days from start to end."""
    _require_date(start)
    _require_date(end)
    return (end - start).days


def is_weekend(moment):
    """Return True when moment falls on Saturday or Sunday."""
    _require_date(moment)
    return moment.weekday() >= 5


def next_weekday(moment):
    """Return the first weekday strictly after moment."""
    _require_date(moment)
    step = timedelta(days=1)
    while (moment + step).weekday() >= 5:
        step += timedelta(days=1)
    return moment + step


def month_length(moment):
    """Return the number of days in the month of moment."""
    _require_date(moment)
    if moment.month == 12:
        following = date(moment.year + 1, 1, 1)
    else:
        following = date(moment.year, moment.month + 1, 1)
    return (following - date(moment.year, moment.month, 1)).days
