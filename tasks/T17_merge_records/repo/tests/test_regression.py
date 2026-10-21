import pytest

from mergekit import (
    complete_record,
    conflicting_fields,
    describe_conflicts,
    field_names,
    fill_missing,
    format_merge,
    format_records,
    group_by_id,
    has_conflict,
    latest_versions,
    merge_field,
    merge_records,
    pick_latest,
    record_key,
    reorder,
    shared_fields,
    sort_by_version,
    stable_order,
    summarize_fields,
    summarize_versions,
    unique_ids,
)


def test_fill_missing_applies_defaults_without_mutation():
    record = {"id": "a", "name": "ana"}
    filled = fill_missing(record)
    assert filled == {"id": "a", "name": "ana", "version": 1, "source": "unknown"}
    assert record == {"id": "a", "name": "ana"}


def test_complete_record():
    record = {"id": "a", "version": 2}
    defaults = {"id": "x", "name": "default", "version": 1}
    assert complete_record(record, defaults) == {
        "id": "a",
        "name": "default",
        "version": 2,
        "source": "unknown",
    }


def test_field_helpers():
    records = [{"id": "a", "name": "ana"}, {"id": "b", "score": 3}]
    assert field_names(records) == ["id", "name", "score"]
    assert shared_fields(records) == ["id"]
    assert shared_fields([]) == []


def test_record_key():
    assert record_key({"id": "a"}) == "a"
    assert record_key({"id": 3}) == 3
    with pytest.raises(KeyError):
        record_key({"name": "ana"})
    with pytest.raises(TypeError):
        record_key({"id": 3.5})


def test_group_by_id():
    records = [{"id": "a"}, {"id": "b"}, {"id": "a"}]
    groups = group_by_id(records)
    assert list(groups) == ["a", "b"]
    assert len(groups["a"]) == 2


def test_merge_records_with_unique_ids():
    records = [
        {"id": "b", "version": 1},
        {"id": "a", "version": 2},
    ]
    merged = merge_records(records)
    assert [record["id"] for record in merged] == ["b", "a"]
    assert merged[1]["version"] == 2


def test_merge_records_with_equal_versions_keeps_the_first():
    records = [
        {"id": "a", "version": 2, "name": "first"},
        {"id": "a", "version": 2, "name": "second"},
    ]
    assert merge_records(records)[0]["name"] == "first"


def test_pick_latest():
    older = {"id": "a", "version": 1}
    newer = {"id": "a", "version": 2}
    assert pick_latest(older, newer) is newer
    assert pick_latest(newer, older) is newer


def test_latest_versions():
    records = [{"id": "a", "version": 1}, {"id": "a", "version": 3}]
    assert latest_versions(records) == {"a": 3}


def test_order_helpers():
    records = [
        {"id": "b", "version": 1},
        {"id": "a", "version": 3},
    ]
    assert [record["id"] for record in stable_order(records)] == ["a", "b"]
    assert [record["id"] for record in sort_by_version(records)] == ["a", "b"]
    assert unique_ids(records) == ["b", "a"]
    assert reorder(records, ["a"]) == [{"id": "a", "version": 3}]


def test_conflicts():
    current = {"id": "a", "name": "old", "version": 1}
    candidate = {"id": "a", "name": "new", "version": 2}
    assert conflicting_fields(current, candidate) == ["name", "version"]
    assert has_conflict(current, candidate) is True
    assert describe_conflicts(current, candidate) == (
        "name: old -> new, version: 1 -> 2"
    )
    assert describe_conflicts(current, current) == "no conflicts"
    assert merge_field(current, candidate, "name") == "new"


def test_format_helpers():
    records = [{"id": "a", "name": "ana", "version": 2}]
    assert format_records(records, ["id", "name"]) == "a | ana"
    assert summarize_fields(records) == "id, name, version"
    assert format_merge(records) == "a:ana"


def test_summarize_versions_with_unique_ids():
    records = [{"id": "a", "version": 2}, {"id": "b", "version": 1}]
    assert summarize_versions(records) == "a=2, b=1"
