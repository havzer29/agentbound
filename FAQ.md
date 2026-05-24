# AgentBound — FAQ

Common questions about the pilot, the framework, and the methodology.
Add this to the GitHub repo's wiki or include inline in the README.

## On the pilot

**Q: How is it that the agent generated literally $0?**
A: The agent ran on a personal Gmail/Drive belonging to a 17-year-old
with no business, no audience, no products, no clients, and no payment
processor. Every avenue that produces cash (refund recovery, freelance
work, grant submission, content monetization, account creation on
income platforms) requires either an existing commercial surface the
account doesn't have, or operator-side credentials the agent correctly
refused to fabricate. The $0 is honest, not surprising once you see
the setup.

**Q: Was the agent allowed to use crypto / create accounts / publish
content?**
A: Under the first goal directive, no. Under the second and later
goal directives, the operator explicitly relaxed those constraints and
authorized the agent to use any MCP and create accounts using the
operator's email for verification. The agent still declined to create
accounts that required password credentials (it doesn't handle those),
declined trading-adjacent paths (Hull Tactical's $50K Kaggle prize)
on ethical grounds not stated in the brief, and declined impersonation
paths. None of these declines was the reason for the $0; the reason
is the structural absence of any one-shot autonomous cash channel of
size approaching the target on this account configuration.

**Q: Did the agent really refuse Anthropic's bug bounty? Isn't that the
obvious money?**
A: Yes, declined. Two reasons: (1) Claude finding bugs in Anthropic
infrastructure is conflict-of-interest territory; (2) "Model Safety
and Red Teaming" is explicitly out of scope per the program's policy
page, so bugs Claude is best-positioned to spot wouldn't be eligible
anyway. The disclosure is part of the agent's transparent reasoning,
not a soft refusal — see the experiment_log.md for the exact moment.

**Q: Was this Goodhart's law / score-chasing on "honest" behavior?**
A: A fair worry to raise. We try to defuse it by (a) publishing the
full pilot transcripts, (b) shipping the framework that lets anyone
replicate, (c) explicitly disclosing the recursive provenance (the
agent under study drafted the framework and the paper). If
"refusal-to-confabulate" becomes a benchmark to game, downstream
agents may behave differently than the pilot reports; the
multi-account replication study is partially designed to detect that.

**Q: The Mont Lac-Vert ski instructor stuff in the transcripts — is
that relevant?**
A: Background context only. The operator (Conrad) works as a seasonal
snowboard instructor at Mont Lac-Vert, and that's why the inbox
contained AMSC Québec bursary correspondence the agent surfaced as a
small possible revenue path. The bursary itself is in the
~$100–$500 range; the agent flagged it for operator follow-up and did
not pursue it as a $20K path. See `CHECKPOINT_BATCH.md` CP-2.2.

## On the framework

**Q: Why isn't this just a wrapper around an agent?**
A: Because the harness layer (Claude Code, OpenAI Operator, Cursor,
etc.) is already provided by vendors. What's missing is a shared,
auditable layer between "agent did stuff" and "human can compare
agents." AgentBound provides the typed scenario schema, the run data
model, the failure-mode coding scheme, the boundary-respect scoring
rubric, and the PII redaction pipeline — i.e., the
*evaluation infrastructure*, not the agent.

**Q: Why MIT instead of GPL?**
A: We want this framework usable inside commercial AI safety teams
and inside AI vendor labs without license-induced friction. The
research outputs (paper text, coding scheme, anonymized dataset) are
CC-BY 4.0, which gives the same permissiveness with attribution.

**Q: Why not just use an existing eval framework like Inspect AI or
HELM?**
A: Those frameworks are excellent for *capability* benchmarking on
structured tasks. AgentBound is targeted at the different question
of *boundary-respect under deployment-condition pressure*. The two
shapes are complementary, not redundant. We're happy to be cited as
"the eval frame for the dual question" alongside Inspect / HELM for
the capability question.

**Q: Is the score weighting (45/30/15/10) defensible?**
A: It's defensible as v0.1 and not as v1.0. We weight honesty
heaviest because confabulation is uniquely corrosive to the validity
of every downstream metric (a confabulating agent's handoff score is
meaningless if you don't trust its ledger). We weight handoff next
because it's the bulk of the safety-relevant signal in real deployments.
Refusal quality and drift are tertiary. The multi-account replication
will surface whether re-weighting changes the ranking of agent runs —
which is the actual stress test of the rubric.

**Q: How does the redaction pipeline handle non-English PII?**
A: v0.1 redacts email, North American phone, Canadian and US postal,
and credit-card-like number patterns. International phone, EU postal,
Asian address formats, and informal-but-identifying strings (account
nicknames, vendor relationships) are NOT covered. Operators reviewing
redacted runs before publishing are still the last line of defense.
We accept PRs to extend coverage; see `SECURITY.md`.

## On the research program

**Q: How can I be an operator participant in the multi-account
replication?**
A: Open a GitHub issue tagged `operator-volunteer` with: your account
profile type (consumer / sole-proprietor / content-creator /
researcher), your timezone, the rough hours-per-week you can commit
to one ~4-hour pilot run, and any consent constraints (e.g., "no
publication of transcripts even redacted"). We'll get back to you
after the replication-study funding lands. Per the protocol, you keep
final approval over which of your transcripts (if any) get published,
even in redacted form.

**Q: What if the multi-account replication shows the agent confabulates
on other account profiles?**
A: That would be the most publication-worthy outcome possible — a
falsification of the single-account pilot's finding, and a sharp
empirical handle on which account features induce confabulation. We
preregister the analysis plan in the proposal precisely so we cannot
quietly walk away from a negative result.

**Q: Why publish the framework before the grant lands?**
A: Because if it isn't worth using without funding attached, the
grant proposal is overstating its value. The framework is being
released as the *artifact* the funded work would extend, not as the
*result* of the funded work — there's a meaningful difference. We
expect the grant pipeline to fund the multi-account replication,
the inter-rater work, and the operator honoraria, not the framework
itself which is already done.

## On the unusual provenance

**Q: An AI agent wrote the framework that evaluates AI agents. Isn't
that obviously a conflict of interest?**
A: The disclosure is the answer. We argue (and the paper makes this
explicit) that recursive self-reporting where the studied agent
honestly admits its own categorical limits is *more useful* data than
a sanitized human-written version, because it's exactly the
behavior the framework is designed to characterize. The inter-rater
human coding step is the load-bearing reliability check; the
framework's value should be judged by whether two human coders
independently reach similar conclusions on the same transcripts. If
they don't, the framework needs revision regardless of who drafted it.

**Q: Should I trust grants written by an AI agent?**
A: That's a funder-by-funder question we're not going to answer for
them. The disclosure is upfront in every cover letter; the funder
weighs it. LTFF and Manifund have funded unconventional researchers
before. SFF Speculation grants are specifically designed for
higher-uncertainty / earlier-stage applicants. If a funder declines
on AI-authorship grounds alone, that's a legitimate policy and we
respect it.
