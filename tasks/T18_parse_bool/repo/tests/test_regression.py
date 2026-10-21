import pytest

from confkit import (
    DEFAULT_CONFIG,
    build_options,
    describe_config,
    describe_env,
    env_name,
    format_bool,
    format_flags,
    format_summary,
    format_value,
    from_env,
    is_true,
    load_config,
    override_config,
    parse_args,
    parse_bool,
    public_config,
    require_keys,
    resolve_config,
    toggle,
    unknown_keys,
    validate_config,
)


def test_parse_bool_python_values():
    assert parse_bool(True) is True
    assert parse_bool(False) is False
    assert parse_bool(1) is True
    assert parse_bool(0) is False


def test_parse_bool_true_words():
    for text in ("1", "true", "yes", "on", " TRUE "):
        assert parse_bool(text) is True


def test_format_bool():
    assert format_bool(True) == "true"
    assert format_bool(False) == "false"
    assert format_bool("yes") == "true"


def test_is_true_and_toggle():
    assert is_true("yes") is True
    assert is_true(0) is False
    assert toggle("yes") is False
    assert toggle(False) is True


def test_load_config_defaults():
    assert load_config() == DEFAULT_CONFIG
    assert load_config() is not DEFAULT_CONFIG


def test_load_config_converts_values():
    config = load_config({"debug": "true", "retries": "5", "name": "demo"})
    assert config == {"debug": True, "retries": 5, "name": "demo"}
    with pytest.raises(TypeError):
        load_config({"retries": True})
    with pytest.raises(TypeError):
        load_config("debug=true")


def test_resolve_config_precedence():
    merged = resolve_config({"debug": "true"}, {"name": "env"})
    assert merged["debug"] is True
    assert merged["name"] == "env"
    assert merged["retries"] == 3


def test_override_and_public_config():
    assert override_config(DEFAULT_CONFIG, "retries", "7")["retries"] == 7
    assert "secret" not in public_config({"secret": "x", "name": "demo"})


def test_cli_parsing():
    assert parse_args(["--debug", "true"]).debug == "true"
    assert build_options(["--debug", "true"])["debug"] is True
    assert build_options(["--retries", "4", "--name", "cli"])["retries"] == 4


def test_validation_helpers():
    assert unknown_keys({"debug": True}) == []
    assert unknown_keys({"extra": 1}) == ["extra"]
    with pytest.raises(KeyError):
        require_keys({}, ["debug", "name"])
    assert validate_config(DEFAULT_CONFIG) == DEFAULT_CONFIG
    with pytest.raises(ValueError):
        validate_config({"debug": True, "extra": 1})


def test_report_helpers():
    assert format_value(True) == "true"
    assert describe_config({"debug": False, "name": "app"}) == "debug=false, name=app"
    assert format_flags({"name": "app"}) == "--name app"
    assert format_summary({"name": "app", "debug": True}) == "name=app debug=on"


def test_env_helpers():
    assert env_name("debug") == "APP_DEBUG"
    values = from_env({"APP_DEBUG": "true", "OTHER": "x"})
    assert values == {"debug": "true"}
    assert load_config(values)["debug"] is True
    assert describe_env({"APP_NAME": "demo"}) == "name=demo"
