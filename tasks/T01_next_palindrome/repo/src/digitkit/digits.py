"""Validation and conversion helpers for decimal digit sequences."""


def validate_digits(digits):
    """Return a list copy of digits after checking every item is 0 to 9."""
    if isinstance(digits, (str, bytes)):
        raise TypeError("digits must be a sequence of integers")
    if not isinstance(digits, (list, tuple)):
        raise TypeError("digits must be a list or tuple")
    if not digits:
        raise ValueError("digits must not be empty")
    result = []
    for digit in digits:
        if isinstance(digit, bool) or not isinstance(digit, int):
            raise TypeError("each digit must be an integer")
        if digit < 0 or digit > 9:
            raise ValueError("each digit must be between 0 and 9")
        result.append(digit)
    return result


def to_digits(value):
    """Return the decimal digits of a non-negative integer."""
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError("value must be an integer")
    if value < 0:
        raise ValueError("value must be non-negative")
    return [int(char) for char in str(value)]


def from_digits(digits):
    """Return the integer represented by a validated digit sequence."""
    prepared = validate_digits(digits)
    return int("".join(str(digit) for digit in prepared))


def mirror_prefix(digits):
    """Return digits with the left half mirrored onto the right half."""
    prepared = validate_digits(digits)
    result = list(prepared)
    for index in range(len(result) // 2):
        result[-1 - index] = result[index]
    return result
