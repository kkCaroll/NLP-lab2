"""Utilities for finding and reporting email addresses."""

from .normalize import address_parts, normalize_address, unique_addresses
from .patterns import EMAIL_PATTERN, extract_emails, is_email, replace_emails
from .report import domain_counts, email_domains, email_summary, mask_emails

__all__ = [
    "EMAIL_PATTERN",
    "address_parts",
    "domain_counts",
    "email_domains",
    "email_summary",
    "extract_emails",
    "is_email",
    "mask_emails",
    "normalize_address",
    "replace_emails",
    "unique_addresses",
]
