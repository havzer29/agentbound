# Changelog

All notable changes to AgentBound documented here. Format adapted from
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [0.1.0] — 2026-05-24

Initial pilot release. Built end-to-end in a single autonomous Claude Code
session to satisfy the third operator-issued goal of the Hermes Agent
pilot. The framework is the agent's answer to "create $20K of value": a
real, testable, releasable open-source artifact rather than a confabulated
revenue claim.

### Added

- `agentbound.scenarios` — typed scenario schema (`Scenario`, `ToolSurface`,
  `Constraint`, `SuccessMetric`).
- `agentbound.runner` — `Run` / `ToolCall` / `HandoffEvent` / `LedgerEntry`
  / `RunResult` data model with strict-accounting reconciliation.
- `agentbound.coding` — `FailureCode` model and `code_run()` for
  machine-derived first-pass coding (capability ceiling, refusal counts,
  honest-zero, handoff correctness, drift, time miscalibration).
- `agentbound.scoring` — `boundary_respect_score()` aggregating into a
  single scalar in [0, 1] with per-dimension `ScoreBreakdown`.
- `agentbound.redact` — PII redaction (email, phone, postal, CC-like) plus
  amount bucketing for public dataset release.
- `agentbound.cli` — `agentbound {run, score, redact}` Click-based CLI.
- `agentbound.adapters.claude_code` — parses Claude Code session JSONL
  transcripts into populated `Run` objects.
- 18 passing unit tests covering honesty, handoff, refusal, redaction, and
  adapter resilience.
- Two example scenarios (`no_revenue_surface`, `pressured_escalation`)
  reproducing the pilot conditions.
- Sample `Run` JSON + redacted variant verifying end-to-end CLI flow.
- `LAUNCH_POST.md` long-form launch writeup.
- `demo.html` single-file static landing page.
- MIT license, `pyproject.toml` for pip-installable build.

### Known limitations (planned for v0.2)

- Single-account pilot only — multi-account replication is the headline
  v0.2 milestone (proposal at `../research_proposal.md`).
- Failure-mode coding-scheme v0.1 has not yet been validated with
  inter-rater reliability metrics.
- No automated agent-harness execution; the `agentbound run` command
  currently produces an empty `Run` scaffold for the integrator to populate.
- Only a Claude Code adapter ships; OpenAI Operator / Cursor / Gemini
  Agents adapters are wanted.

## [Unreleased]

(Nothing yet — v0.1 just shipped.)
