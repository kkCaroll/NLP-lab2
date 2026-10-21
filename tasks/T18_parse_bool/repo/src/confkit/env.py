"""Environment style configuration helpers."""

from .validate import KNOWN_KEYS

PREFIX = "APP_"


def env_name(key):
    """Return the environment variable name for a configuration key."""
    return PREFIX + key.upper()


def from_env(environ):
    """Extract known configuration keys from an environment mapping."""
    if not isinstance(environ, dict):
        raise TypeError("environ must be a dictionary")
    values = {}
    for key in sorted(KNOWN_KEYS):
        name = env_name(key)
        if name in environ:
            values[key] = environ[name]
    return values


def describe_env(environ):
    """Render the recognised environment values as text."""
    values = from_env(environ)
    return ", ".join(f"{key}={values[key]}" for key in sorted(values))
