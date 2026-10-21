"""Configuration loading with defaults and type conversion."""

from .booleans import parse_bool

DEFAULT_CONFIG = {
    "debug": False,
    "retries": 3,
    "name": "app",
}


def load_config(values=None):
    """Return configuration with defaults and converted types."""
    if values is None:
        return dict(DEFAULT_CONFIG)
    if not isinstance(values, dict):
        raise TypeError("values must be a dictionary")
    config = dict(DEFAULT_CONFIG)
    for key, value in values.items():
        if key == "debug":
            config[key] = parse_bool(value)
        elif key == "retries":
            if isinstance(value, bool):
                raise TypeError("retries must be an integer")
            config[key] = int(value)
        else:
            config[key] = value
    return config


def resolve_config(file_values, env_values=None):
    """Merge environment values over file values and load the result."""
    if env_values is None:
        env_values = {}
    if not isinstance(file_values, dict) or not isinstance(env_values, dict):
        raise TypeError("configuration sources must be dictionaries")
    merged = dict(file_values)
    merged.update(env_values)
    return load_config(merged)


def override_config(config, key, value):
    """Return a copy of config with one key overridden and converted."""
    if not isinstance(config, dict):
        raise TypeError("config must be a dictionary")
    updated = dict(config)
    updated[key] = value
    return load_config(updated)


def public_config(config):
    """Return configuration entries that are safe to display."""
    if not isinstance(config, dict):
        raise TypeError("config must be a dictionary")
    return {
        key: value
        for key, value in config.items()
        if key != "secret"
    }
