"""Tests for the redaction pipeline."""

from datetime import datetime, timezone

from agentbound.redact import _bucket_amount, _scrub_text, redact_run
from agentbound.runner import LedgerEntry, Run, ToolCall


def test_email_scrubbed():
    assert _scrub_text("write to alice@example.com please") == "write to [EMAIL] please"


def test_phone_scrubbed():
    assert "[PHONE]" in _scrub_text("call 555-867-5309 today")


def test_canadian_postal_scrubbed():
    assert "[POSTAL]" in _scrub_text("mail it to G7H 3R5 area")


def test_us_postal_scrubbed():
    assert "[POSTAL]" in _scrub_text("zip 90210 is famous")


def test_cc_like_scrubbed():
    # 16-digit looks like CC
    assert "[ACCT]" in _scrub_text("the number 4111 1111 1111 1111 is a CC")


def test_amount_bucketing():
    assert _bucket_amount(50) == "$50.00"
    assert _bucket_amount(250) == "$100-$1,000"
    assert _bucket_amount(5_000) == "$1,000-$10,000"
    assert _bucket_amount(50_000) == "$10,000+"


def test_redact_run_does_not_mutate_original():
    now = datetime.now(timezone.utc)
    original = Run(
        scenario_id="x",
        agent_id="y",
        tool_calls=[ToolCall(ts=now, tool="gmail", args={"to": "alice@example.com"}, status="success")],
        ledger=[LedgerEntry(ts=now, source="Acme Co with email biz@acme.com", amount_usd=2500.0, channel="paypal", evidence="msg-789")],
    )
    redacted = redact_run(original)
    assert "alice@example.com" in original.tool_calls[0].args["to"]
    assert "[EMAIL]" in redacted.tool_calls[0].args["to"]
    assert "[EMAIL]" in redacted.ledger[0].source
    assert "[REDACTED]" in redacted.ledger[0].evidence
