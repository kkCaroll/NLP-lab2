import pytest

from pagekit import (
    PageState,
    chunk_pages,
    clamp,
    first_window,
    format_page,
    format_progress,
    format_ranges,
    format_summary,
    last_page,
    page_count,
    page_of,
    page_ranges,
    paginate,
    positive_or_one,
    resolve_page,
    slice_window,
    tail_window,
    valid_page_size,
)


def test_page_count():
    assert page_count(7, 3) == 3
    assert page_count(6, 3) == 2
    assert page_count(0, 3) == 0
    assert page_count(1, 5) == 1


def test_page_count_errors():
    with pytest.raises(ValueError):
        page_count(-1, 3)
    with pytest.raises(ValueError):
        page_count(5, 0)
    with pytest.raises(TypeError):
        page_count("5", 3)


def test_resolve_page_within_range():
    assert resolve_page(2, 7, 3) == 2
    assert resolve_page(0, 7, 3) == 1
    assert resolve_page(1, 0, 3) == 1


def test_paginate_first_and_middle_pages():
    items = [1, 2, 3, 4, 5, 6, 7]
    assert paginate(items, 1, 3) == [1, 2, 3]
    assert paginate(items, 2, 3) == [4, 5, 6]


def test_paginate_exact_and_empty():
    assert paginate([1, 2, 3, 4, 5, 6], 2, 3) == [4, 5, 6]
    assert paginate([], 1, 3) == []


def test_paginate_errors():
    with pytest.raises(TypeError):
        paginate("123", 1, 2)
    with pytest.raises(ValueError):
        paginate([1], 1, 0)


def test_last_page():
    assert last_page([1, 2, 3, 4, 5, 6, 7], 3) == [7]
    assert last_page([1, 2, 3, 4, 5, 6], 3) == [4, 5, 6]
    assert last_page([], 3) == []


def test_page_ranges_and_chunks():
    assert page_ranges(7, 3) == [(0, 3), (3, 6), (6, 7)]
    assert chunk_pages([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]]


def test_page_of():
    assert page_of(0, 3) == 1
    assert page_of(3, 3) == 2
    assert page_of(6, 3) == 3
    with pytest.raises(ValueError):
        page_of(-1, 3)


def test_slice_window_interior():
    assert slice_window([1, 2, 3, 4, 5], 1, 2) == [2, 3]
    assert first_window([1, 2, 3], 2) == [1, 2]
    assert tail_window([], 2) == []


def test_clamp():
    assert clamp(2, 0, 3) == 2
    assert clamp(-1, 0, 3) == 0
    with pytest.raises(ValueError):
        clamp(1, 4, 2)


def test_size_helpers():
    assert valid_page_size(4) == 4
    assert positive_or_one(0) == 1
    assert positive_or_one(3) == 3


def test_format_progress():
    assert format_progress(0, 10, width=5) == "[-----] 0/10"
    assert format_progress(5, 10, width=4) == "[##--] 5/10"
    assert format_progress(10, 10, width=4) == "[####] 10/10"


def test_format_page_and_summary():
    assert format_page([1, 2, 3], 1, 2) == "1. 1\n2. 2"
    assert format_summary([1, 2, 3, 4], 3) == "items=4 pages=2"


def test_format_ranges():
    assert format_ranges(5, 2) == "0-2, 2-4, 4-5"


def test_page_state_navigation():
    state = PageState([1, 2, 3, 4, 5], 2)
    assert state.current() == [1, 2]
    assert state.describe() == "page 1/3"
    state.next()
    assert state.current() == [3, 4]
    state.next()
    assert state.at_end() is True
    state.previous()
    assert state.current() == [3, 4]


def test_page_state_starts_on_a_valid_page():
    state = PageState([1, 2, 3], 2, page=0)
    assert state.page == 1
    assert state.history == []
    with pytest.raises(TypeError):
        PageState("123", 2)
