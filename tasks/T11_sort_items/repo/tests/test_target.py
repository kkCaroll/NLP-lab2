from listkit import sort_items


def test_sort_items_returns_the_sorted_values():
    assert sort_items([3, 1, 2]) == [1, 2, 3]


def test_sort_items_does_not_reorder_the_input():
    values = [3, 1, 2]
    sort_items(values, reverse=True)
    assert values == [3, 1, 2]
