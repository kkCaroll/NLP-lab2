"""Text rendering for configuration values."""

from .booleans import format_bool


def format_value(value):
    """Render one configuration value."""
    if isinstance(value, bool):
        return format_bool(value)
    return str(value)


def describe_config(config):
    """Render configuration entries in key order."""
    if not isinstance(config, dict):
        raise TypeError("config must be a dictionary")
    return ", ".join(
        f"{key}={format_value(config[key])}" for key in sorted(config)
    )


def format_flags(config):
    """Render configuration entries as command line flags."""
    if not isinstance(config, dict):
        raise TypeError("config must be a dictionary")
    flags = []
    for key in sorted(config):
        flags.append(f"--{key}")
        flags.append(format_value(config[key]))
    return " ".join(flags)


def format_summary(config):
    """Render a short description of configuration state."""
    if not isinstance(config, dict):
        raise TypeError("config must be a dictionary")
    debug = "on" if config.get("debug") else "off"
    return f"name={config.get('name', 'app')} debug={debug}"
