from recordkit import department_age_order, sort_records, top_k

ROSTER = [
    {"id": "e1", "name": "Cara", "age": 25, "department": "research"},
    {"id": "e2", "name": "bob", "age": 30, "department": "research"},
    {"id": "e3", "name": "Ana", "age": 30, "department": "operations"},
    {"id": "e4", "name": "dave", "age": 41, "department": "operations"},
]


def test_sort_records_orders_age_descending_then_name_ascending():
    names = [record["name"] for record in sort_records(ROSTER)]
    assert names == ["dave", "Ana", "bob", "Cara"]


def test_top_k_and_department_order_share_multi_key_order():
    assert [record["name"] for record in top_k(ROSTER, 2)] == ["dave", "Ana"]
    assert department_age_order(ROSTER)["research"] == ["bob", "Cara"]
