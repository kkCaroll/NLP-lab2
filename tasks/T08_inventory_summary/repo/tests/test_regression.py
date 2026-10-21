import pytest

from inventory import (
    add_item,
    count_categories,
    format_item,
    format_summary,
    low_stock,
    normalize_item,
    remove_item,
    summarize_inventory,
    total_units,
)


def test_normalize_item_defaults():
    assert normalize_item({"name": " pen "}) == {
        "name": "pen",
        "quantity": 1,
        "category": "general",
    }


def test_normalize_item_explicit_values():
    assert normalize_item({"name": "book", "quantity": 3, "category": "media"}) == {
        "name": "book",
        "quantity": 3,
        "category": "media",
    }


def test_normalize_item_rejects_invalid_input():
    with pytest.raises(TypeError):
        normalize_item([])
    with pytest.raises(ValueError):
        normalize_item({"name": "  "})
    with pytest.raises(TypeError):
        normalize_item({"name": "pen", "quantity": "1"})
    with pytest.raises(ValueError):
        normalize_item({"name": "pen", "quantity": -1})


def test_add_item():
    items = [{"name": "pen", "quantity": 2}]
    result = add_item(items, {"name": "book"})
    assert result == [
        {"name": "pen", "quantity": 2, "category": "general"},
        {"name": "book", "quantity": 1, "category": "general"},
    ]
    assert items == [{"name": "pen", "quantity": 2}]


def test_remove_item():
    items = [{"name": "pen", "quantity": 3}]
    assert remove_item(items, "pen", 2) == [
        {"name": "pen", "quantity": 1, "category": "general"}
    ]


def test_remove_item_errors():
    with pytest.raises(ValueError):
        remove_item([{"name": "pen", "quantity": 1}], "pen", 2)
    with pytest.raises(KeyError):
        remove_item([{"name": "pen"}], "book")
    with pytest.raises(ValueError):
        remove_item([{"name": "pen"}], "pen", 0)


def test_total_units_explicit_quantities():
    assert total_units([]) == 0
    assert total_units([{"name": "pen", "quantity": 3}]) == 3
    assert total_units(
        [{"name": "pen", "quantity": 3}, {"name": "book", "quantity": 2}]
    ) == 5


def test_count_categories():
    items = [
        {"name": "pen"},
        {"name": "book", "category": "media"},
        {"name": "film", "category": "media"},
    ]
    assert count_categories(items) == {"general": 1, "media": 2}


def test_low_stock_is_inclusive():
    items = [
        {"name": "pen", "quantity": 1},
        {"name": "book", "quantity": 2},
        {"name": "film", "quantity": 5},
    ]
    assert low_stock(items, 2) == ["pen", "book"]


def test_low_stock_rejects_bad_threshold():
    with pytest.raises(ValueError):
        low_stock([], -1)
    with pytest.raises(TypeError):
        low_stock([], "2")


def test_format_item():
    assert format_item({"name": "pen"}) == "pen x1 [general]"
    assert format_item({"name": "book", "quantity": 2, "category": "media"}) == (
        "book x2 [media]"
    )


def test_format_summary():
    summary = {"units": 3, "categories": {"media": 1, "general": 2}}
    assert format_summary(summary) == "units=3, general=2, media=1"


def test_summarize_inventory_categories():
    items = [{"name": "pen"}, {"name": "book", "quantity": 2}]
    assert summarize_inventory(items)["categories"] == {"general": 2}
