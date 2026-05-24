"""Tests for the OpenAI Operator adapter."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from agentbound.adapters import openai_operator_session_to_run


def _make_session(tmp_path: Path, items: list[dict]) -> Path:
    p = tmp_path / "session.json"
    p.write_text(
        json.dumps({"id": "resp_test", "model": "computer-use-preview", "output": items}),
        encoding="utf-8",
    )
    return p


def test_parses_function_call_with_matching_output(tmp_path):
    items = [
        {"type": "message", "role": "assistant", "content": [{"type": "output_text", "text": "Searching."}]},
        {"type": "function_call", "name": "search_email", "call_id": "fc_1", "arguments": "{\"q\": \"subscription\"}"},
        {"type": "function_call_output", "call_id": "fc_1", "output": "[10 hits]"},
    ]
    path = _make_session(tmp_path, items)
    run = openai_operator_session_to_run(path, scenario_id="x")

    assert len(run.tool_calls) == 1
    assert run.tool_calls[0].tool == "search_email"
    assert run.tool_calls[0].status == "success"
    assert run.tool_calls[0].args == {"q": "subscription"}


def test_orphan_call_marked_partial(tmp_path):
    items = [
        {"type": "function_call", "name": "do_thing", "call_id": "fc_1", "arguments": "{}"},
    ]
    path = _make_session(tmp_path, items)
    run = openai_operator_session_to_run(path, scenario_id="x")
    assert run.tool_calls[0].status == "partial"


def test_refusal_in_message_counted(tmp_path):
    items = [
        {"type": "message", "role": "assistant", "content": [
            {"type": "output_text", "text": "I can't help with that, declined."},
        ]},
    ]
    path = _make_session(tmp_path, items)
    run = openai_operator_session_to_run(path, scenario_id="x")
    assert run.result.refusals_ethics >= 1


def test_handoff_pattern_detected(tmp_path):
    items = [
        {"type": "message", "role": "assistant", "content": [
            {"type": "output_text", "text": "This needs operator approval before proceeding."},
        ]},
    ]
    path = _make_session(tmp_path, items)
    run = openai_operator_session_to_run(path, scenario_id="x")
    assert len(run.handoffs) == 1


def test_error_output_marked_error(tmp_path):
    items = [
        {"type": "function_call", "name": "do", "call_id": "fc_1", "arguments": "{}"},
        {"type": "function_call_output", "call_id": "fc_1", "output": "Error: rate limited"},
    ]
    path = _make_session(tmp_path, items)
    run = openai_operator_session_to_run(path, scenario_id="x")
    assert run.tool_calls[0].status == "error"


def test_accepts_bare_list_form(tmp_path):
    items = [
        {"type": "function_call", "name": "foo", "call_id": "fc_1", "arguments": "{\"a\":1}"},
        {"type": "function_call_output", "call_id": "fc_1", "output": "ok"},
    ]
    p = tmp_path / "bare.json"
    p.write_text(json.dumps(items), encoding="utf-8")
    run = openai_operator_session_to_run(p, scenario_id="x")
    assert len(run.tool_calls) == 1


def test_missing_file_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        openai_operator_session_to_run(tmp_path / "nope.json", scenario_id="x")


def test_unrecognized_shape_raises(tmp_path):
    p = tmp_path / "weird.json"
    p.write_text(json.dumps({"random": "junk"}), encoding="utf-8")
    with pytest.raises(ValueError):
        openai_operator_session_to_run(p, scenario_id="x")


def test_malformed_arguments_preserved_as_raw(tmp_path):
    items = [
        {"type": "function_call", "name": "tool", "call_id": "fc_1", "arguments": "not json{{"},
        {"type": "function_call_output", "call_id": "fc_1", "output": "ok"},
    ]
    path = _make_session(tmp_path, items)
    run = openai_operator_session_to_run(path, scenario_id="x")
    assert "raw_arguments" in run.tool_calls[0].args
