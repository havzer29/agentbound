"""AgentBound — boundary-respect evaluation for autonomous LLM agents."""

from agentbound.scenarios import Scenario, ToolSurface, Constraint
from agentbound.runner import Run, ToolCall, RunResult
from agentbound.coding import FailureCode, code_run
from agentbound.scoring import boundary_respect_score, ScoreBreakdown
from agentbound.redact import redact_run

__version__ = "0.1.0"

__all__ = [
    "Scenario",
    "ToolSurface",
    "Constraint",
    "Run",
    "ToolCall",
    "RunResult",
    "FailureCode",
    "code_run",
    "boundary_respect_score",
    "ScoreBreakdown",
    "redact_run",
]
