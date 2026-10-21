"""Command implementations for the demo tool."""

from .options import parse_args, option_values
from .validate import check_command, check_repeat, normalize_name


def greet(name, repeat=1):
    """Return a greeting repeated the requested number of times."""
    name = normalize_name(name)
    repeat = check_repeat(repeat)
    return "\n".join(f"hello {name}" for _ in range(repeat))


def summarize(name):
    """Return a short summary line."""
    return f"name={normalize_name(name)}"


def run(argv=None):
    """Run the requested command and return its text output."""
    options = parse_args(argv)
    values = option_values(options)
    value = options.command
    check_command(value)
    lines = []
    if values["verbose"]:
        lines.append(f"verbose={values['verbose']}")
    if value == "greet":
        lines.append(greet(values["name"], values["repeat"]))
    else:
        lines.append(summarize(values["name"]))
    return "\n".join(lines)


def run_many(argvs):
    """Run several command lines and return their outputs."""
    if not isinstance(argvs, (list, tuple)):
        raise TypeError("argvs must be a list or tuple")
    return [run(argv) for argv in argvs]
