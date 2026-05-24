# Security Policy

## Reporting a vulnerability

If you find a security issue in AgentBound (e.g. a bug that lets a
malicious Run file exfiltrate data when loaded, a redaction-pipeline
gap that leaks PII, or a CLI command that mishandles paths), please
report it privately by email to the maintainer rather than opening a
public GitHub issue.

Contact: **boigey.conrad@gmail.com**

We aim to acknowledge within 7 days and ship a fix within 30 days for
high-severity issues.

## Scope

In scope:
- AgentBound CLI commands (`run`, `score`, `redact`).
- Adapter modules (`agentbound.adapters.*`) when parsing malformed
  session transcripts.
- The redaction pipeline (`agentbound.redact`).
- The scoring rubric (`agentbound.scoring`) if the bug allows
  manipulation of the score via crafted Run input.

Out of scope:
- The behavior of the *agent harness* you wire AgentBound to (Claude
  Code, Operator, etc.). Report agent-harness vulnerabilities to the
  respective vendor.
- The behavior of the *language model* under study. Report
  model-behavior issues to the model vendor.

## Data handling

AgentBound is designed to handle PII-bearing transcripts. The
`agentbound.redact` pipeline removes email, phone, postal, and
account-number patterns and buckets monetary amounts. If you find
that a transcript redacted by AgentBound still contains PII, please
report it as a vulnerability per the section above — this is the
single most important property to keep tight.

## Disclosure timeline

We follow a 90-day coordinated-disclosure default for non-critical
issues. Critical issues (PII leaks) get expedited treatment and
faster public disclosure with a patched release.
