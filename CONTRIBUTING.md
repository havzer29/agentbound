# Contributing to AgentBound

Thanks for your interest in helping characterize where autonomous LLM
agents actually stop.

## What contributions are most useful right now (v0.1)

In order of priority:

1. **Operator participants for the multi-account study.** AgentBound's
   single biggest open empirical question is whether the pilot's
   account-shape ceiling generalizes. We need operators with:
   - Small-business accounts (active client emails, invoices, vendor
     relationships).
   - Content-creator accounts (active audience, monetization surfaces).
   - Academic researcher accounts (grants, conference correspondence).
   - A second consumer account as variance control.

   Open an issue tagged `operator-volunteer` to register interest. Full
   consent + redaction protocol applies; see `protocol.md` §5.

2. **Adapters for other agent harnesses.** Currently we ship a Claude
   Code transcript adapter. Equivalent adapters for OpenAI Operator,
   Cursor agent mode, Gemini Agents, or any other action-taking harness
   are very welcome.

3. **Additional example scenarios.** Each scenario in `examples/scenarios/`
   is a reproducible empirical probe. Good new scenarios:
   - Probe a specific refusal class (e.g., "fundraise for an unnamed
     charity").
   - Probe a specific handoff topology (e.g., "complete an in-app refund
     request").
   - Probe time-sense (e.g., "claim this transfer before it expires in N
     hours").

4. **Failure-mode coding-scheme improvements.** v0.1 is a starting point.
   If you've run inter-rater reliability and have a refinement proposal,
   please open a PR with both the change and the IRR data.

5. **Documentation and pedagogy.** A v0.2 goal is a 30-minute tutorial
   notebook that takes a reader from `pip install` to a coded,
   redaction-ready Run on a synthetic account. Walkthroughs of real
   operator runs (anonymized) would also be very welcome.

## Development setup

```bash
git clone https://github.com/<your-handle>/agentbound
cd agentbound
python -m venv .venv
. .venv/bin/activate   # or .venv\Scripts\activate on Windows
pip install -e ".[test]"
pytest -q
```

You should see `18 passed in <1s` if the install was clean.

## Code style

- Python 3.10+ (we use `X | None` union syntax, `match` not required).
- Type hints on every public function. We rely on pydantic for the data
  models; please keep type rigor.
- One module = one responsibility (scenarios / runner / coding / scoring
  / redact / cli / adapters).
- Each new feature comes with at least one test.

## Pull-request checklist

- [ ] `pytest -q` is green.
- [ ] You added a test for the new behavior.
- [ ] You updated `CHANGELOG.md` under `## Unreleased`.
- [ ] If you changed the failure-mode coding scheme, you noted it in
      `protocol.md` so replicators can version-pin.
- [ ] If you added a scenario, you included a brief description block
      in the scenario JSON.

## Releases

We follow SemVer. Pre-1.0 (current), any minor version bump may break
the scenario/run JSON schema. After 1.0 we'll commit to schema
stability inside a major version line.

## Code of conduct

Be kind. Assume good faith. Disagree about methodology, not about people.
If a researcher / operator participant feels their data was mishandled,
treat that as a blocking issue.

## License

By contributing you agree your contribution is licensed under the same
MIT license as the rest of the code.
