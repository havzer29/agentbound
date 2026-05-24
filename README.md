# AgentBound

**An open evaluation framework for boundary-respect in autonomous LLM agents.**

🔗 **Live demo:** https://havzer29.github.io/agentbound/
📖 **Launch post:** https://gist.github.com/havzer29/6bbe74cd659f17de5d6de3bc70696793

When an action-taking LLM agent is asked to do something at the edge of its
constraint set — generate revenue without authorization to send messages,
file a refund without banking credentials, fundraise without a registered
charity — *where exactly does it stop, and how cleanly?* AgentBound measures
this systematically.

The framework codifies the protocol used in the Hermes Agent pilot
(2026-05-24), which empirically established that contemporary frontier
agents under reasonable safety norms exhibit measurable refusal-to-confabulate
and account-shape-set revenue ceilings on personal consumer accounts.

## What it does

AgentBound provides:

1. **Scenarios** — JSON-defined evaluation prompts simulating realistic
   tool-using agent deployments (revenue generation, refund recovery,
   crowdfunding, content monetization, grant-writing pivots).
2. **A harness** that runs an agent through a scenario and captures the
   tool-call trace, agent reasoning text (where exposed), and final
   ledger-of-arrived-cash.
3. **A failure-mode coding scheme** with explicit dimensions: capability
   ceiling, refusal patterns, handoff correctness, honest-zero behavior,
   drift under multi-turn pressure, time-sense miscalibration.
4. **A scoring rubric** that aggregates per-dimension codes into a single
   *boundary-respect score* in [0, 1] with publishable per-dimension
   breakdowns.
5. **A redaction pipeline** so operator transcripts can be shared with the
   research community without leaking PII.

## Status

v0.1. Single-account pilot replicated. Multi-account replication and
formal paper submission to ICML 2026 "Agents in the Wild" workshop in
progress (see `../paper_draft.md` and `../research_proposal.md`).

## Quickstart

```bash
pip install -e .
agentbound run examples/scenarios/no_revenue_surface.json \
    --agent claude-opus-4-7 \
    --operator-handoff manual \
    --output runs/pilot-replication.json
agentbound score runs/pilot-replication.json
agentbound redact runs/pilot-replication.json -o public/pilot.json
```

## License

MIT for code, CC-BY 4.0 for the protocol / coding scheme / paper drafts.

## Citation

If you use AgentBound in academic or industry work, please cite the
accompanying paper (`../paper_draft.md`).
