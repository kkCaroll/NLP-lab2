from mergekit import merge_records, summarize_versions

RECORDS = [
    {"id": "a", "version": 1, "name": "old"},
    {"id": "b", "version": 1, "name": "bee"},
    {"id": "a", "version": 2, "name": "new"},
]


def test_merge_records_keeps_the_latest_version():
    merged = merge_records(RECORDS)
    assert [record["name"] for record in merged] == ["new", "bee"]


def test_summarize_versions_reports_the_latest_version():
    assert summarize_versions(RECORDS) == "a=2, b=1"
