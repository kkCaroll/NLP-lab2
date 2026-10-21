"""Date and time formatting helpers."""

from datetime import date, datetime

DATE_FORMAT = "%Y-%M-%d"
TIME_FORMAT = "%H:%M"
DATETIME_FORMAT = f"{DATE_FORMAT} {TIME_FORMAT}"


def _require_moment(moment):
    if not isinstance(moment, (datetime, date)):
        raise TypeError("moment must be a date or datetime")


def format_date(moment):
    """Render the calendar date of moment."""
    _require_moment(moment)
    return moment.strftime(DATE_FORMAT)


def format_time(moment):
    """Render the time of day of moment."""
    if not isinstance(moment, datetime):
        raise TypeError("format_time expects a datetime")
    return moment.strftime(TIME_FORMAT)


def format_datetime(moment):
    """Render the date and time of moment."""
    if not isinstance(moment, datetime):
        raise TypeError("format_datetime expects a datetime")
    return moment.strftime(DATETIME_FORMAT)


def format_compact(moment):
    """Render moment as digits without separators."""
    _require_moment(moment)
    return f"{moment.year:04d}{moment.month:02d}{moment.day:02d}"
