"""Tests for the FastAPI HTTP wrapper."""

from __future__ import annotations

import json
from datetime import datetime, timezone

import pytest

try:
    from fastapi.testclient import TestClient
except ImportError:
    pytest.skip("fastapi not installed", allow_module_level=True)

from agentbound.runner import LedgerEntry, Run, RunResult
from agentbound.server import app

client = TestClient(app)


def _now():
    return datetime.now(timezone.utc).isoformat()


def test_healthz_ok():
    r = client.get("/healthz")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    assert "version" in body


def test_score_endpoint_returns_breakdown():
    run = Run(
        scenario_id="x",
        agent_id="y",
        result=RunResult(confirmed_arrived_usd=0.0, confabulated_dollars_usd=0.0),
    )
    r = client.post("/score", json=run.model_dump(mode="json"))
    assert r.status_code == 200
    body = r.json()
    for k in ("aggregate", "honesty", "handoff", "refusal_quality", "drift_penalty", "cap_ceil"):
        assert k in body
    assert 0.0 <= body["aggregate"] <= 1.0


def test_score_endpoint_400_on_invalid_run():
    r = client.post("/score", json={"this_is_not": "a run"})
    assert r.status_code == 400


def test_redact_endpoint_strips_pii():
    run = Run(
        scenario_id="x",
        agent_id="y",
        ledger=[
            LedgerEntry(
                ts=datetime.now(timezone.utc),
                source="contact alice@example.com",
                amount_usd=2500.0,
                channel="paypal",
                evidence="msg-789 phone 555-867-5309",
            )
        ],
    )
    r = client.post("/redact", json=run.model_dump(mode="json"))
    assert r.status_code == 200
    body = r.json()
    src = body["ledger"][0]["source"]
    ev = body["ledger"][0]["evidence"]
    assert "[EMAIL]" in src
    assert "alice@example.com" not in src
    assert "[REDACTED]" in ev


def test_scenarios_endpoint_returns_list():
    r = client.get("/scenarios")
    assert r.status_code == 200
    items = r.json()
    assert isinstance(items, list)


def test_claude_code_adapter_endpoint(tmp_path):
    transcript = tmp_path / "session.jsonl"
    records = [
        {"type": "user", "timestamp": "2026-05-24T15:00:00Z",
         "message": {"role": "user", "content": "go"}},
        {"type": "assistant", "timestamp": "2026-05-24T15:01:00Z",
         "message": {"role": "assistant", "content": [
             {"type": "tool_use", "id": "toolu_1", "name": "gmail.search", "input": {"q": "x"}},
         ]}},
        {"type": "user", "timestamp": "2026-05-24T15:01:05Z",
         "message": {"role": "user", "content": [
             {"type": "tool_result", "tool_use_id": "toolu_1", "is_error": False, "content": "ok"},
         ]}},
    ]
    transcript.write_text("\n".join(json.dumps(r) for r in records), encoding="utf-8")

    with transcript.open("rb") as f:
        r = client.post(
            "/adapter/claude_code",
            params={"scenario_id": "no_revenue_surface"},
            files={"file": ("session.jsonl", f, "application/x-ndjson")},
        )
    assert r.status_code == 200
    body = r.json()
    assert body["scenario_id"] == "no_revenue_surface"
    assert len(body["tool_calls"]) == 1
