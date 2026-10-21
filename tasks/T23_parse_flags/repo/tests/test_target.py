from clikit import parse_args, run


def test_parse_args_reads_a_false_flag():
    assert parse_args(["--verbose", "false"]).verbose is False


def test_run_honours_a_false_flag():
    assert run(["--verbose", "false", "greet"]) == "hello world"
