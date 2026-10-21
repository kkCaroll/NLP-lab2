"""Regular expressions for recognising version strings."""

import re

VERSION_PATTERN = re.compile(
    r"(?<![\w.-])v?(\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?)"
)
VERSION_EXACT = re.compile(r"^v?\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?$")


def extract_versions(text):
    """Return version strings found in text, without a leading v."""
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    return VERSION_PATTERN.findall(text)


def find_version_positions(text):
    """Return start, end and text of each version found in text."""
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    return [
        (match.start(1), match.end(1), match.group(1))
        for match in VERSION_PATTERN.finditer(text)
    ]


def is_version(text):
    """Return True when text is exactly one version string."""
    if not isinstance(text, str):
        return False
    return VERSION_EXACT.fullmatch(text) is not None


def has_prerelease(version):
    """Return True when a version carries a prerelease suffix."""
    if not isinstance(version, str):
        raise TypeError("version must be a string")
    return "-" in version


def replace_versions(text, replacement):
    """Return text with every recognised version replaced."""
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    if not isinstance(replacement, str):
        raise TypeError("replacement must be a string")
    return VERSION_PATTERN.sub(replacement, text)
