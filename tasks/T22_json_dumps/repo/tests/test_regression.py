import pytest

from payloadkit import (
    PayloadError,
    build_envelope,
    count_non_ascii,
    describe_flat,
    describe_payload,
    describe_size,
    ensure_text,
    envelope_ok,
    error_envelope,
    flatten_mapping,
    format_payload,
    has_non_ascii,
    is_json_text,
    json_bytes,
    json_dumps,
    json_loads,
    json_safe,
    merge_payloads,
    normalize_payload,
    parse_envelope,
    pick_fields,
    sort_payload,
    summarize_keys,
    wrap_items,
)


def test_json_roundtrip():
    payload = {"name": "ana", "items": [1, 2], "ok": True}
    assert json_loads(json_dumps(payload)) == payload
    assert json_loads(json_dumps({"name": "ana"})) == {"name": "ana"}


def test_json_roundtrip_unicode():
    payload = {"name": "安娜", "note": "café"}
    assert json_loads(json_dumps(payload)) == payload
    assert json_loads(json_bytes(payload).decode("utf-8")) == payload


def test_json_errors():
    with pytest.raises(PayloadError):
        json_dumps(object())
    with pytest.raises(PayloadError):
        json_loads("{broken")
    with pytest.raises(TypeError):
        json_loads(b"{}")
    assert is_json_text("{}") is True
    assert is_json_text("{broken") is False


def test_text_helpers():
    assert ensure_text(b"caf\xc3\xa9") == "café"
    assert ensure_text("plain") == "plain"
    with pytest.raises(TypeError):
        ensure_text(3)
    assert has_non_ascii("café") is True
    assert has_non_ascii("cafe") is False
    assert count_non_ascii("café") == 1


def test_sort_and_safe_payload():
    payload = {"b": {"z": 1, "a": 2}, "a": [3]}
    assert sort_payload(payload) == {"a": [3], "b": {"a": 2, "z": 1}}
    assert json_safe({"name": "ana", "pair": (1, 2)}) == {
        "name": "ana",
        "pair": [1, 2],
    }


def test_normalise_helpers():
    assert normalize_payload((1, 2)) == [1, 2]
    nested = {"b": {"y": 2, "x": 1}, "a": 3}
    assert flatten_mapping(nested) == {"a": 3, "b.x": 1, "b.y": 2}
    assert merge_payloads({"a": 1}, {"b": 2}) == {"a": 1, "b": 2}
    assert pick_fields({"a": 1, "b": 2}, ["b", "c"]) == {"b": 2}


def test_envelope_roundtrip():
    text = build_envelope({"value": 3})
    assert parse_envelope(text) == {"ok": True, "data": {"value": 3}}
    assert envelope_ok(text) is True
    assert parse_envelope(error_envelope("bad"))["ok"] is False
    assert parse_envelope(wrap_items([1, 2]))["data"]["count"] == 2


def test_envelope_errors():
    with pytest.raises(TypeError):
        build_envelope({}, ok="yes")
    with pytest.raises(ValueError):
        parse_envelope("[]")
    with pytest.raises(ValueError):
        parse_envelope('{"ok": true}')


def test_report_helpers():
    assert describe_payload({"a": 1}) == "object with 1 keys"
    assert describe_payload([1, 2]) == "array with 2 items"
    assert describe_payload(3) == "value of type int"
    assert summarize_keys({"b": 1, "a": 2}) == "a, b"
    assert describe_flat({"a": {"b": 1}}) == "a.b=1"
    assert describe_size([1, 2, 3]) == 3
    assert json_loads(format_payload({"a": 1})) == {"a": 1}
