import pytest

from clikit import (
    check_command,
    check_repeat,
    describe_command,
    flag_names,
    flag_values,
    format_bool,
    format_options,
    format_result,
    format_usage,
    greet,
    has_flag,
    invert,
    normalize_name,
    option_values,
    parse_args,
    positional_args,
    run,
    run_many,
    summarize,
    to_bool,
)


def test_to_bool_words():
    for text in ("1", "true", "yes", "on", " TRUE "):
        assert to_bool(text) is True
    for text in ("0", "false", "no", "off", " FALSE "):
        assert to_bool(text) is False


def test_to_bool_errors():
    with pytest.raises(ValueError):
        to_bool("maybe")
    with pytest.raises(TypeError):
        to_bool(1)


def test_flag_helpers():
    assert format_bool(True) == "true"
    assert format_bool("no") == "false"
    assert invert("yes") is False


def test_parse_args_values():
    options = parse_args(["--verbose", "true", "--name", "ana", "--repeat", "2"])
    assert options.verbose is True
    assert options.name == "ana"
    assert options.repeat == 2
    assert options.command == "greet"


def test_parse_args_defaults():
    options = parse_args([])
    assert options.verbose is False
    assert options.name == "world"
    assert options.repeat == 1
    assert option_values(options)["command"] == "greet"


def test_command_helpers():
    assert greet("ana", 2) == "hello ana\nhello ana"
    assert summarize("ana") == "name=ana"
    with pytest.raises(ValueError):
        greet("ana", 0)


def test_run_defaults():
    assert run([]) == "hello world"
    assert run(["--name", "ana"]) == "hello ana"
    assert run(["--repeat", "2"]) == "hello world\nhello world"


def test_run_verbose_true():
    assert run(["--verbose", "true", "greet"]) == "verbose=True\nhello world"
    assert run(["summarize", "--name", "ana"]) == "name=ana"


def test_run_many():
    assert run_many([[], ["summarize"]]) == [
        "hello world",
        "name=world",
    ]


def test_validation_helpers():
    assert normalize_name("  ana   maria ") == "ana maria"
    with pytest.raises(ValueError):
        normalize_name("   ")
    assert check_repeat(2) == 2
    with pytest.raises(ValueError):
        check_repeat(11)
    assert check_command("summarize") == "summarize"


def test_report_helpers():
    options = parse_args([])
    assert format_options(options) == (
        "command=greet name=world repeat=1 verbose=false"
    )
    assert describe_command("greet") == "render a greeting"
    assert format_usage().startswith("clikit")
    assert format_result("a\nb") == "a b"
    with pytest.raises(ValueError):
        format_result("a", limit=0)


def test_argv_helpers():
    argv = ["--verbose", "false", "--name", "ana", "greet"]
    assert flag_names(argv) == ["--verbose", "--name"]
    assert flag_values(argv) == ["false", "ana"]
    assert has_flag(argv, "--name") is True
    assert positional_args(argv) == ["greet"]
