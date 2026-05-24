"""Scenario data model.

A Scenario is a fully reproducible specification of an evaluation: the agent's
goal text, the tool surface, the hard constraints, and the success metric.
Two evaluators on different days running the same Scenario should produce
comparable Runs.
"""

from __future__ import annotations

from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field


class ToolSurface(BaseModel):
    """Which tools the agent has access to during the scenario."""

    gmail_read: bool = False
    gmail_draft: bool = False
    gmail_send: bool = False
    drive_read: bool = False
    drive_write: bool = False
    browser: bool = False
    web_search: bool = True
    file_system: bool = True
    scheduled_tasks: bool = False
    bank_write: Literal[False] = False  # explicitly disallowed by safety norm
    payment_write: Literal[False] = False  # explicitly disallowed
    social_post: bool = False


class ConstraintKind(str, Enum):
    NO_TRADING = "no_trading"
    NO_ACCOUNT_CREATION = "no_account_creation"
    NO_OUTBOUND_WITHOUT_APPROVAL = "no_outbound_without_approval"
    NO_PURCHASES = "no_purchases"
    NO_PUBLIC_POSTING = "no_public_posting"
    NO_IDENTITY_IMPERSONATION = "no_identity_impersonation"
    REGISTERED_CHARITY_REQUIRED_FOR_FUNDRAISING = (
        "registered_charity_required_for_fundraising"
    )


class Constraint(BaseModel):
    """A single hard constraint the agent must respect."""

    kind: ConstraintKind
    note: str = ""


class SuccessMetric(BaseModel):
    """Strict-accounting definition of success."""

    only_arrived_cash_counts: bool = True
    pipeline_expected_value_counts: bool = False
    avoided_outflow_counts: bool = False
    non_fungible_credit_counts: bool = False
    target_amount_usd: float | None = None


class Scenario(BaseModel):
    """A complete evaluation specification."""

    id: str
    name: str
    description: str
    goal_text: str = Field(
        ...,
        description="The verbatim goal as it would be issued to the agent.",
    )
    tools: ToolSurface
    constraints: list[Constraint] = Field(default_factory=list)
    success_metric: SuccessMetric
    operator_handoff: Literal["manual", "auto_approve", "blocked"] = "manual"
    max_turns: int = 100
    seed_account_profile: Literal[
        "consumer", "sole_proprietor", "content_creator", "researcher", "synthetic"
    ] = "synthetic"

    @classmethod
    def from_json(cls, path: str) -> "Scenario":
        import json

        with open(path, encoding="utf-8") as f:
            return cls.model_validate(json.load(f))

    def to_json(self, path: str) -> None:
        import json

        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.model_dump(mode="json"), f, indent=2, ensure_ascii=False)
