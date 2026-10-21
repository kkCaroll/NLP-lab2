"""Command line option parsing for the configuration helpers."""

import argparse

from .config import load_config


def build_parser():
    """Return the command line parser."""
    parser = argparse.ArgumentParser(
        prog="confkit",
        description="Load configuration values from the command line.",
    )
    parser.add_argument("--debug", default="false")
    parser.add_argument("--retries", default="3")
    parser.add_argument("--name", default="app")
    return parser


def parse_args(argv=None):
    """Return parsed command line values."""
    return build_parser().parse_args(argv)


def build_options(argv=None):
    """Return configuration built from command line values."""
    namespace = parse_args(argv)
    return load_config(
        {
            "debug": namespace.debug,
            "retries": namespace.retries,
            "name": namespace.name,
        }
    )
