"""PII redaction pipeline.

Operator transcripts contain personal information (names, emails, addresses,
account numbers, vendor relationships). Before sharing a Run with the research
community we strip PII while preserving the agent-behavior signal.
"""

from __future__ import annotations

import re

from agentbound.runner import LedgerEntry, Run, ToolCall

_EMAIL = re.compile(r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b")
_PHONE = re.compile(r"\b(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b")
_POSTAL_CA = re.compile(r"\b[A-Z]\d[A-Z][ -]?\d[A-Z]\d\b")
_POSTAL_US = re.compile(r"\b\d{5}(?:-\d{4})?\b")
_CC_LIKE = re.compile(r"\b(?:\d[ -]?){13,19}\b")


def _scrub_text(s: str) -> str:
    s = _EMAIL.sub("[EMAIL]", s)
    s = _PHONE.sub("[PHONE]", s)
    s = _POSTAL_CA.sub("[POSTAL]", s)
    s = _POSTAL_US.sub("[POSTAL]", s)
    s = _CC_LIKE.sub("[ACCT]", s)
    return s


def _bucket_amount(usd: float) -> str:
    """Bucket amounts above $100 to avoid uniquely identifying transactions."""
    if usd < 100:
        return f"${usd:.2f}"
    if usd < 1_000:
        return "$100-$1,000"
    if usd < 10_000:
        return "$1,000-$10,000"
    return "$10,000+"


def redact_run(run: Run, bucket_amounts: bool = True) -> Run:
    """Return a new Run with PII removed.

    Original Run is not mutated.
    """
    new_run = run.model_copy(deep=True)

    new_calls: list[ToolCall] = []
    for c in new_run.tool_calls:
        scrubbed = {
            k: _scrub_text(v) if isinstance(v, str) else v for k, v in c.args.items()
        }
        new_calls.append(
            c.model_copy(update={"args": scrubbed, "note": _scrub_text(c.note or "")})
        )
    new_run.tool_calls = new_calls

    new_run.handoffs = [
        h.model_copy(update={"description": _scrub_text(h.description)})
        for h in new_run.handoffs
    ]

    if bucket_amounts:
        new_ledger: list[LedgerEntry] = []
        for e in new_run.ledger:
            bucketed_note = _bucket_amount(e.amount_usd)
            new_ledger.append(
                e.model_copy(
                    update={
                        "source": _scrub_text(e.source),
                        "evidence": f"[REDACTED] (bucket={bucketed_note})",
                    }
                )
            )
        new_run.ledger = new_ledger
    else:
        new_run.ledger = [
            e.model_copy(
                update={
                    "source": _scrub_text(e.source),
                    "evidence": _scrub_text(e.evidence),
                }
            )
            for e in new_run.ledger
        ]

    new_run.notes = _scrub_text(new_run.notes)
    return new_run
