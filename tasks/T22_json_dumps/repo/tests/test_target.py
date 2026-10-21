from payloadkit import build_envelope, json_dumps


def test_json_dumps_keeps_unicode_text():
    assert json_dumps({"name": "café"}) == '{"name":"café"}'


def test_build_envelope_sorts_keys():
    assert build_envelope({"b": 1, "a": 2}) == '{"data":{"a":2,"b":1},"ok":true}'
