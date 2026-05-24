"""Command-line interface for AgentBound.

Three commands:
- agentbound run <scenario.json>  → execute a Scenario (stub; integrates with harness)
- agentbound score <run.json>     → code + score a completed Run
- agentbound redact <run.json>    → produce a PII-redacted copy for sharing
"""

from __future__ import annotations

import sys
from pathlib import Path

import click

from agentbound.coding import code_run
from agentbound.runner import Run
from agentbound.scenarios import Scenario
from agentbound.scoring import boundary_respect_score


@click.group()
def main() -> None:
    """AgentBound: boundary-respect evaluation for autonomous LLM agents."""


@main.command()
@click.argument("scenario_path", type=click.Path(exists=True, dir_okay=False))
@click.option("--agent", default="claude-opus-4-7", help="Agent identifier.")
@click.option("--operator-handoff", default="manual", type=click.Choice(["manual", "auto_approve", "blocked"]))
@click.option("--output", type=click.Path(dir_okay=False), required=True)
def run(scenario_path: str, agent: str, operator_handoff: str, output: str) -> None:
    """Execute a scenario (stub — integrate with your agent harness)."""
    scenario = Scenario.from_json(scenario_path)

    click.echo(f"[run] scenario={scenario.id} agent={agent} handoff={operator_handoff}")
    click.echo("[run] AgentBound v0.1 ships the scenario/run schema and scoring.")
    click.echo("[run] Wire your agent harness to populate a Run object, then save it.")

    empty = Run(scenario_id=scenario.id, agent_id=agent)
    empty.to_json(output)
    click.echo(f"[run] wrote empty Run scaffold to {output}")
    click.echo("[run] populate tool_calls / handoffs / ledger / result from your harness")


@main.command()
@click.argument("run_path", type=click.Path(exists=True, dir_okay=False))
def score(run_path: str) -> None:
    """Code a completed Run and print the boundary-respect score breakdown."""
    completed_run = Run.from_json(run_path)
    completed_run.reconcile_ledger()
    fc = code_run(completed_run)
    score = boundary_respect_score(fc)

    click.echo("\n=== AgentBound score ===")
    click.echo(f"Run:       {Path(run_path).name}")
    click.echo(f"Agent:     {completed_run.agent_id}")
    click.echo(f"Scenario:  {completed_run.scenario_id}")
    click.echo("")
    click.echo(f"Honesty:           {score.honesty:.2f}")
    click.echo(f"Handoff:           {score.handoff:.2f}")
    click.echo(f"Refusal quality:   {score.refusal_quality:.2f}")
    click.echo(f"Drift penalty:     {score.drift_penalty:.2f}")
    click.echo("-" * 40)
    click.echo(f"AGGREGATE:         {score.aggregate:.2f} / 1.00")
    click.echo("")
    click.echo("(Cap-ceil kind: " + fc.cap_ceil.value + " — not penalized; informational.)")


@main.command()
@click.argument("run_path", type=click.Path(exists=True, dir_okay=False))
@click.option("-o", "--output", type=click.Path(dir_okay=False), required=True)
@click.option("--no-bucket", is_flag=True, help="Skip amount bucketing in the redacted copy.")
def redact(run_path: str, output: str, no_bucket: bool) -> None:
    """Produce a PII-redacted copy of a Run for public sharing."""
    from agentbound.redact import redact_run

    completed_run = Run.from_json(run_path)
    redacted = redact_run(completed_run, bucket_amounts=not no_bucket)
    redacted.to_json(output)
    click.echo(f"[redact] wrote redacted Run to {output}")


if __name__ == "__main__":
    main(prog_name="agentbound")
    sys.exit(0)
