from inventory import summarize_inventory, total_units


def test_total_units_counts_an_omitted_quantity_as_one():
    items = [{"name": "pen"}, {"name": "book", "quantity": 2}]
    assert total_units(items) == 3


def test_summary_uses_the_default_quantity():
    items = [{"name": "pen"}, {"name": "book", "quantity": 2}]
    assert summarize_inventory(items)["units"] == 3
