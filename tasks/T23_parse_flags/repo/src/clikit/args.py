"""Low level helpers for command line argument lists."""


def require_argv(argv):
    """Return argv after checking that it is a sequence of strings."""
    if not isinstance(argv, (list, tuple)):
        raise TypeError("argv must be a list or tuple")
    for item in argv:
        if not isinstance(item, str):
            raise TypeError("argv entries must be strings")
    return list(argv)


def flag_names(argv):
    """Return option names in order of appearance."""
    return [item for item in require_argv(argv) if item.startswith("--")]


def flag_values(argv):
    """Return the values that follow option names."""
    items = require_argv(argv)
    values = []
    for index, item in enumerate(items[:-1]):
        if item.startswith("--") and not items[index + 1].startswith("--"):
            values.append(items[index + 1])
    return values


def has_flag(argv, name):
    """Return True when the option name appears in argv."""
    if not isinstance(name, str) or not name.startswith("--"):
        raise ValueError("name must be an option name")
    return name in require_argv(argv)


def positional_args(argv):
    """Return positional arguments with option values removed."""
    items = require_argv(argv)
    result = []
    skip = False
    for index, item in enumerate(items):
        if skip:
            skip = False
            continue
        if item.startswith("--"):
            if index + 1 < len(items) and not items[index + 1].startswith("--"):
                skip = True
            continue
        result.append(item)
    return result
