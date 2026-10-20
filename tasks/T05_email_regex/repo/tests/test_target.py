from mailscan.patterns import extract_emails, is_email, replace_emails
from mailscan.report import domain_counts, email_summary


def test_extract_emails_with_plus_tag():
    text = "contact alice+news@example.com and bob@example.org"
    assert extract_emails(text) == ["alice+news@example.com", "bob@example.org"]
    assert is_email("alice+news@example.com")
    assert replace_emails(text) == "contact [email] and [email]"


def test_report_helpers_include_plus_tag():
    text = "alice+news@example.com, alice+alerts@example.com, bob@other.org"
    assert domain_counts(text) == {"example.com": 2, "other.org": 1}
    summary = email_summary(text)
    assert summary["count"] == 3
    assert summary["domains"] == ["example.com", "other.org"]
    assert summary["masked"] == "[redacted], [redacted], [redacted]"
