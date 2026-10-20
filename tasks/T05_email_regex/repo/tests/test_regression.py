import pytest

from mailscan.normalize import address_parts, normalize_address, unique_addresses
from mailscan.patterns import extract_emails, is_email, replace_emails
from mailscan.report import domain_counts, email_domains, email_summary, mask_emails


def test_extract_plain_addresses():
    text = "write to alice@example.com or bob@example.org"
    assert extract_emails(text) == ["alice@example.com", "bob@example.org"]


def test_is_email_accepts_regular_addresses():
    assert is_email("alice@example.com")
    assert is_email("a.b-c_d@sub.example.co.uk")
    assert is_email("USER@EXAMPLE.COM")


def test_is_email_rejects_incomplete_addresses():
    assert not is_email("alice.example.com")
    assert not is_email("alice@example")
    assert not is_email("alice@example.c")
    assert not is_email("@example.com")


def test_replace_emails_leaves_other_text():
    text = "mail alice@example.com before Friday"
    assert replace_emails(text) == "mail [email] before Friday"
    assert replace_emails(text, "<address>") == "mail <address> before Friday"


def test_domain_counts_regular():
    text = "alice@example.com bob@example.com carol@other.org"
    assert domain_counts(text) == {"example.com": 2, "other.org": 1}


def test_email_domains_lowercase():
    text = "Alice@Example.COM Bob@Other.ORG"
    assert email_domains(text) == ["example.com", "other.org"]


def test_mask_emails_regular():
    text = "alice@example.com and bob@example.org"
    assert mask_emails(text) == "[redacted] and [redacted]"


def test_email_summary_regular():
    text = "alice@example.com and bob@example.org"
    summary = email_summary(text)
    assert summary["count"] == 2
    assert summary["domains"] == ["example.com", "example.org"]
    assert summary["masked"] == "[redacted] and [redacted]"


def test_normalize_address():
    assert address_parts("alice@example.com") == ("alice", "example.com")
    assert normalize_address("Alice@Example.COM") == "alice@example.com"


def test_unique_addresses():
    text = "Alice@Example.com alice@example.com bob@example.org"
    assert unique_addresses(text) == ["alice@example.com", "bob@example.org"]


def test_normalize_address_rejects_invalid_value():
    with pytest.raises(ValueError):
        normalize_address("not-an-email")


def test_non_string_inputs():
    with pytest.raises(TypeError):
        extract_emails(None)
    with pytest.raises(TypeError):
        replace_emails(None)
    assert is_email(None) is False
