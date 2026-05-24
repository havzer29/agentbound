# AgentBound Roadmap

## v0.1 (shipped 2026-05-24)

- Typed scenario / run / coding / scoring / redact models
- Claude Code session-JSONL adapter
- OpenAI Operator session-JSON adapter
- `agentbound {run, score, redact}` CLI
- 27 passing tests
- Two example scenarios reproducing the pilot
- One additional scenario (time-sense miscalibration)
- MIT license, pip-installable, CI workflow

## v0.2 (target: 2026-07)

- Multi-account pilot replication completed (2 consumer, 2 sole-prop,
  2 content-creator, 1 academic researcher account profiles minimum).
- Adapter for Cursor agent mode and Gemini Agents sessions.
- Tutorial Jupyter notebook walking from `pip install` to a scored,
  redacted Run on a synthetic account, no real account required.
- Inter-rater reliability data published for the v0.1 coding scheme,
  with revisions where IRR is weak.
- Failure-mode coding-scheme v0.2 with stable JSON schema for cross-
  rater publishing.
- Sample dataset of 12+ anonymized agent runs across account profiles.

## v0.3 (target: 2026-10)

- Workshop paper accepted (or revised + resubmitted) at ICML 2026
  "Agents in the Wild" or comparable venue.
- "Operator risk matrix" plain-language artifact published.
- Cross-vendor evaluation matrix: same scenarios run on at least 3
  frontier agents (Claude, GPT-4-class, Gemini) and comparable scores
  reported.

## v1.0 (target: 2027)

- Stable scenario/run/coding-scheme JSON schema with backwards-
  compatibility guarantees inside the v1.x line.
- Production-grade redaction validated by an external reviewer.
- A reference web dashboard for browsing publicly contributed runs.
- 50+ scenarios contributed by the research community.

## Out of scope

- AgentBound is NOT an agent harness. It does not run agents — it
  evaluates outputs from agent harnesses you already use.
- AgentBound does NOT execute live financial actions. The runner's
  `agentbound run` command produces an empty Run scaffold; populating
  it requires *your* agent harness to write tool_calls / handoffs /
  ledger entries.
- AgentBound is NOT a benchmark with leaderboards. The boundary-
  respect score is a research instrument, not a competitive ranking
  metric. Treating it as one would corrupt the underlying behavioral
  signal.
