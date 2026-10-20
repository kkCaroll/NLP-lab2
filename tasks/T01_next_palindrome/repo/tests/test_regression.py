import pytest

from digitkit.digits import from_digits, mirror_prefix, to_digits, validate_digits
from digitkit.palindrome import is_palindrome, next_palindrome, next_palindrome_int
from digitkit.report import describe_next_palindrome, next_palindrome_length


def test_next_palindrome_examples():
    assert next_palindrome([1, 4, 9, 4, 1]) == [1, 5, 0, 5, 1]
    assert next_palindrome([1, 3, 1]) == [1, 4, 1]
    assert next_palindrome([4, 7, 2, 5, 5, 2, 7, 4]) == [4, 7, 2, 6, 6, 2, 7, 4]
    assert next_palindrome([4, 7, 2, 5, 2, 7, 4]) == [4, 7, 2, 6, 2, 7, 4]


def test_next_palindrome_regular_carry():
    assert next_palindrome([1, 9, 1]) == [2, 0, 2]
    assert next_palindrome([9, 8, 9]) == [9, 9, 9]
    assert next_palindrome([1, 9, 9, 1]) == [2, 0, 0, 2]


def test_next_palindrome_single_digit():
    assert next_palindrome([0]) == [1]
    assert next_palindrome([8]) == [9]


def test_is_palindrome():
    assert is_palindrome(0)
    assert is_palindrome(121)
    assert is_palindrome(1221)
    assert not is_palindrome(123)
    assert not is_palindrome(10)


def test_next_palindrome_int_regular():
    assert next_palindrome_int(191) == 202
    assert next_palindrome_int(12321) == 12421
    assert next_palindrome_int(1991) == 2002


def test_validate_digits_regular():
    assert validate_digits([0, 9, 5]) == [0, 9, 5]
    assert validate_digits((1, 2, 1)) == [1, 2, 1]


def test_validate_digits_rejects_invalid():
    with pytest.raises(TypeError):
        validate_digits("121")
    with pytest.raises(TypeError):
        validate_digits([1, True, 1])
    with pytest.raises(ValueError):
        validate_digits([])
    with pytest.raises(ValueError):
        validate_digits([1, 10, 1])


def test_to_digits_and_from_digits():
    assert to_digits(1201) == [1, 2, 0, 1]
    assert to_digits(0) == [0]
    assert from_digits([1, 0, 1]) == 101


def test_mirror_prefix():
    assert mirror_prefix([1, 2, 3, 4, 5]) == [1, 2, 3, 2, 1]
    assert mirror_prefix([4, 7, 2, 5, 5, 2, 7, 4]) == [4, 7, 2, 5, 5, 2, 7, 4]


def test_describe_next_palindrome_regular():
    assert describe_next_palindrome(191) == "191 -> 202"
    assert describe_next_palindrome(12321) == "12321 -> 12421"


def test_next_palindrome_length_regular():
    assert next_palindrome_length(191) == 3
    assert next_palindrome_length(12321) == 5
