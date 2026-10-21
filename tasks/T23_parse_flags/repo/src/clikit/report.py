"""Text rendering for command line options."""

from .flags import format_bool


def format_options(options):
    """Render parsed options in a fixed order."""
    return (
        f"command={options.command} name={options.name} "
        f"repeat={options.repeat} verbose={format_bool(options.verbose)}"
    )


def describe_command(command):
    """Return a short description of a command."""
    descriptions = {
        "greet": "render a greeting",
        "summarize": "render a summary",
    }
    return descriptions.get(command, "unknown command")


def format_usage():
    """Return a short usage line."""
    return "clikit [--verbose BOOL] [--name NAME] [--repeat N] [greet|summarize]"


def format_result(output, limit=60):
    """Return output shortened to a single display line."""
    if isinstance(limit, bool) or not isinstance(limit, int):
        raise TypeError("limit must be an integer")
    if limit < 1:
        raise ValueError("limit must be positive")
    text = " ".join(output.split())
    if len(text) <= limit:
        return text
    return text[: limit - 1] + "…"
