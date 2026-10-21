"""Command line parser construction."""

import argparse


def build_parser():
    """Return the command line parser for the demo tool."""
    parser = argparse.ArgumentParser(
        prog="clikit",
        description="Render a greeting or a short summary.",
    )
    parser.add_argument("--verbose", type=bool, default=False)
    parser.add_argument("--name", default="world")
    parser.add_argument("--repeat", type=int, default=1)
    parser.add_argument(
        "command",
        nargs="?",
        choices=("greet", "summarize"),
        default="greet",
    )
    return parser


def parse_args(argv=None):
    """Return parsed command line options."""
    return build_parser().parse_args(argv)


def option_values(options):
    """Return the option values as a dictionary."""
    return {
        "verbose": options.verbose,
        "name": options.name,
        "repeat": options.repeat,
        "command": options.command,
    }
