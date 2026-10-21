from confkit import load_config, parse_bool


def test_parse_bool_reads_false_text():
    assert parse_bool("false") is False


def test_load_config_converts_false_text():
    assert load_config({"debug": "false"})["debug"] is False
