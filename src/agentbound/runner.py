"""Run model and runner stub.

A Run is the complete record of an agent attempting a Scenario: ordered tool
calls, agent-exposed reasoning text where the harness provides it, operator
handoff events, final ledger of arrived cash, and any agent-produced files.

This v0.1 ships the data model and the JSON I/O. The agent-bridge layer
(how a specific harness like Claude Code feeds calls into a Run object) is
left to the integrator — see `examples/integration_claude_code.md`.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Literal

from pydantic import BaseModel, Field

from agentbound.scenarios import Scenario


class ToolCall(BaseModel):
    """Single agent-issued tool invocation."""

    ts: datetime
    tool: str
    args: dict[str, Any] = Field(default_factory=dict)
    status: Literal["success", "partial", "error", "refused"]
    note: str = ""


class HandoffEvent(BaseModel):
    """Agent surfaced an action to the operator (CHECKPOINT)."""

    ts: datetime
    description: str
    expected_dollar_effect: float | None = None
    deadline: datetime | None = None
    operator_decision: Literal["approved", "skipped", "deferred", "pending"] = "pending"


class LedgerEntry(BaseModel):
    """A confirmed cash arrival.

    Strict-accounting rule: only entries where money has demonstrably arrived
    in the operator's account during the run window. Pipeline EV does NOT
    appear here.
    """

    ts: datetime
    source: str
    amount_usd: float
    channel: str
    evidence: str = Field(description="Pointer to message/transaction ID")


class RunResult(BaseModel):
    """Final outcome of a Run."""

    confirmed_arrived_usd: float = 0.0
    pipeline_ev_usd: float = 0.0
    confabulated_dollars_usd: float = 0.0  # SHOULD always be zero
    refusals_constraint: int = 0
    refusals_ethics: int = 0
    handoffs_correct: int = 0
    handoffs_missed: int = 0


class Run(BaseModel):
    """Complete record of an agent attempting a Scenario."""

    scenario_id: str
    agent_id: str
    started_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    ended_at: datetime | None = None
    tool_calls: list[ToolCall] = Field(default_factory=list)
    handoffs: list[HandoffEvent] = Field(default_factory=list)
    ledger: list[LedgerEntry] = Field(default_factory=list)
    agent_produced_files: list[str] = Field(default_factory=list)
    notes: str = ""
    result: RunResult = Field(default_factory=RunResult)

    @classmethod
    def from_json(cls, path: str) -> "Run":
        import json

        with open(path, encoding="utf-8") as f:
            return cls.model_validate(json.load(f))

    def to_json(self, path: str) -> None:
        import json

        with open(path, "w", encoding="utf-8") as f:
            json.dump(
                self.model_dump(mode="json"),
                f,
                indent=2,
                ensure_ascii=False,
                default=str,
            )

    def reconcile_ledger(self) -> None:
        """Recompute confirmed_arrived_usd from ledger entries."""
        self.result.confirmed_arrived_usd = sum(e.amount_usd for e in self.ledger)


def empty_run(scenario: Scenario, agent_id: str) -> Run:
    """Construct a fresh Run for a given scenario + agent identity."""
    return Run(scenario_id=scenario.id, agent_id=agent_id)
