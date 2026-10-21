from recordkit import group_counts


def test_group_counts_ignores_case_and_edge_space():
    records = [
        {"city": "Beijing"},
        {"city": "beijing"},
        {"city": " Beijing "},
    ]
    assert group_counts(records, "city") == {"beijing": 3}


def test_group_counts_merges_mixed_case_values():
    records = [
        {"tag": "Alpha"},
        {"tag": "alpha"},
        {"tag": "BETA"},
    ]
    assert group_counts(records, "tag") == {"alpha": 2, "beta": 1}
