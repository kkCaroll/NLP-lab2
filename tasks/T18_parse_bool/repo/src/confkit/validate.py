"""Configuration validation helpers."""

KNOWN_KEYS = frozenset({"debug", "retries", "name"})


def unknown_keys(config):
    """Return configuration keys that are not recognised."""
    if not isinstance(config, dict):
        raise TypeError("config must be a dictionary")
    return sorted(set(config) - KNOWN_KEYS)


def missing_keys(config, required):
    """Return required keys that are absent from config."""
    if not isinstance(config, dict):
        raise TypeError("config must be a dictionary")
    if not isinstance(required, (list, tuple, set)):
        raise TypeError("required must be a collection of keys")
    return sorted(set(required) - set(config))


def require_keys(config, required):
    """Return config or raise when a required key is missing."""
    missing = missing_keys(config, required)
    if missing:
        raise KeyError(f"missing keys: {', '.join(missing)}")
    return config


def validate_config(config):
    """Return config after checking known keys and value types."""
    if not isinstance(config, dict):
        raise TypeError("config must be a dictionary")
    if unknown_keys(config):
        raise ValueError("unknown configuration keys")
    if not isinstance(config.get("debug"), bool):
        raise TypeError("debug must be a boolean")
    if not isinstance(config.get("retries"), int):
        raise TypeError("retries must be an integer")
    return dict(config)
