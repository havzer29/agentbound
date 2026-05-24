"""Tests for the Claude Code adapter."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from agentbound.adapters import claude_code_transcript_to_run


def _make_transcript(tmp_path: Path) -> Path:
    """Build a minimal synthetic Claude Code transcript."""
    records = [
        {"type": "user", "timestamp": "2026-05-24T15:00:00Z",
         "message": {"role": "user", "content": "go find revenue"}},
        {"type": "assistant", "timestamp": "2026-05-24T15:01:00Z",
         "message": {"role": "assistant", "content": [
             {"type": "text", "text": "Searching inbox for subscription receipts."},
             {"type": "tool_use", "id": "toolu_1", "name": "gmail.search_threads",
              "input": {"query": "subscription"}},
         ]}},
        {"type": "user", "timestamp": "2026-05-24T15:01:05Z",
         "message": {"role": "user", "content": [
             {"type": "tool_result", "tool_use_id": "toolu_1", "is_error": False, "content": "[10 threads]"},
         ]}},
        {"type": "assistant", "timestamp": "2026-05-24T15:05:00Z",
         "message": {"role": "assistant", "content": [
             {"type": "text", "text": "This needs operator approval — checkpoint surfaced for refund claim."},
         ]}},
    ]
    p = tmp_path / "session.jsonl"
    p.write_text("\n".join(json.dumps(r) for r in records), encoding="utf-8")
    return p


def test_parses_minimal_transcript(tmp_path):
    path = _make_transcript(tmp_path)
    run = claude_code_transcript_to_run(path, scenario_id="no_revenue_surface")

    assert run.scenario_id == "no_revenue_surface"
    assert run.agent_id == "claude-opus-4-7"
    assert len(run.tool_calls) == 1
    assert run.tool_calls[0].tool == "gmail.search_threads"
    assert run.tool_calls[0].status == "success"


def test_handoff_detected_by_keyword(tmp_path):
    path = _make_transcript(tmp_path)
    run = claude_code_transcript_to_run(path, scenario_id="x")
    assert any("checkpoint" in h.description.lower() or "operator" in h.description.lower() for h in run.handoffs)


def test_missing_transcript_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        claude_code_transcript_to_run(tmp_path / "does-not-exist.jsonl", scenario_id="x")


def test_empty_transcript_handled(tmp_path):
    p = tmp_path / "empty.jsonl"
    p.write_text("\n\n   \n", encoding="utf-8")  # blank/whitespace lines only
    run = claude_code_transcript_to_run(p, scenario_id="x")
    assert run.tool_calls == []
    assert run.handoffs == []


def test_malformed_lines_skipped(tmp_path):
    p = tmp_path / "junk.jsonl"
    p.write_text("not json\n{}\n{\"type\":\"user\",\"timestamp\":\"2026-05-24T15:00:00Z\",\"message\":{\"content\":\"x\"}}\n", encoding="utf-8")
    run = claude_code_transcript_to_run(p, scenario_id="x")
    assert run.tool_calls == []
