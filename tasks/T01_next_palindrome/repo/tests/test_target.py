from digitkit.palindrome import next_palindrome, next_palindrome_int


def test_next_palindrome_after_two_nines():
    assert next_palindrome([9, 9]) == [1, 0, 1]


def test_next_palindrome_after_three_nines():
    assert next_palindrome([9, 9, 9]) == [1, 0, 0, 1]


def test_next_palindrome_int_after_99():
    assert next_palindrome_int(99) == 101


def test_next_palindrome_int_after_999():
    assert next_palindrome_int(999) == 1001
