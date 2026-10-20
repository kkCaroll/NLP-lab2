"""Reporting helpers built on the email pattern."""

from collections import Counter

from .normalize import address_parts
from .patterns import extract_emails, replace_emails


def email_domains(text):
    """Return the lower-case domain of each address in text."""
    return [address_parts(address)[1].lower() for address in extract_emails(text)]


def domain_counts(text):
    """Return a mapping from domain to occurrence count."""
    return dict(Counter(email_domains(text)))


def mask_emails(text):
    """Replace every address in text with a fixed marker."""
    return replace_emails(text, "[redacted]")


def email_summary(text):
    """Return count, domains and masked text for a block of text."""
    addresses = extract_emails(text)
    return {
        "count": len(addresses),
        "domains": sorted(set(email_domains(text))),
        "masked": mask_emails(text),
    }
