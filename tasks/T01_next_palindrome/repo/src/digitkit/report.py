"""Formatting helpers for palindrome transitions."""

from .digits import from_digits, to_digits
from .palindrome import next_palindrome


def describe_next_palindrome(value):
    """Return a short description of the next palindrome after value."""
    result = next_palindrome(to_digits(value))
    return f"{value} -> {from_digits(result)}"


def palindrome_summary(values):
    """Return transition descriptions for each non-negative integer."""
    return [describe_next_palindrome(value) for value in values]


def next_palindrome_length(value):
    """Return the number of digits in the next palindrome after value."""
    result = next_palindrome(to_digits(value))
    return len(result)
