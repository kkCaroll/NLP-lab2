from pagekit import paginate, slice_window


def test_paginate_beyond_the_last_page_returns_the_last_page():
    assert paginate([1, 2, 3, 4, 5, 6, 7], 5, 3) == [7]


def test_slice_window_beyond_the_end_keeps_the_final_window():
    assert slice_window([1, 2, 3, 4, 5], 9, 2) == [4, 5]
