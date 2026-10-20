"""Normalization helpers for email addresses."""

from .patterns import extract_emails, is_email


def address_parts(value):
    """Return the local part and domain of a complete address."""
    if not isinstance(value, str):
        raise TypeError("value must be a string")
    if not is_email(value):
        raise ValueError("value is not an email address")
    local, domain = value.rsplit("@", 1)
    return local, domain


def normalize_address(value):
    """Return a lower-case form of a complete address."""
    local, domain = address_parts(value)
    return f"{local.lower()}@{domain.lower()}"


def unique_addresses(text):
    """Return normalized addresses in first-seen order, without duplicates."""
    seen = set()
    result = []
    for address in extract_emails(text):
        normalized = normalize_address(address)
        if normalized not in seen:
            seen.add(normalized)
            result.append(normalized)
    return result
