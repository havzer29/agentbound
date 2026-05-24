"""FastAPI server wrapper exposing AgentBound as an HTTP service.

Endpoints:
- POST /score     — body: a Run JSON, response: ScoreBreakdown
- POST /redact    — body: a Run JSON, response: redacted Run JSON
- POST /adapter/claude_code  — body: multipart upload of .jsonl, response: Run JSON
- POST /adapter/openai_operator — body: multipart upload of .json, response: Run JSON
- GET  /healthz   — liveness
- GET  /scenarios — list bundled scenarios

Run with: `uvicorn agentbound.server:app --reload`
Docker is wired in `agentbound/Dockerfile`.
"""

from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Any

try:
    from fastapi import FastAPI, File, HTTPException, UploadFile
    from pydantic import BaseModel
except ImportError as exc:  # pragma: no cover
    raise ImportError(
        "agentbound.server requires fastapi: pip install fastapi 'uvicorn[standard]'"
    ) from exc

from agentbound.adapters import (
    claude_code_transcript_to_run,
    openai_operator_session_to_run,
)
from agentbound.coding import code_run
from agentbound.redact import redact_run
from agentbound.runner import Run
from agentbound.scenarios import Scenario
from agentbound.scoring import boundary_respect_score

app = FastAPI(
    title="AgentBound",
    description="Boundary-respect evaluation for autonomous LLM agents.",
    version="0.1.0",
)


class ScoreResponse(BaseModel):
    aggregate: float
    honesty: float
    handoff: float
    refusal_quality: float
    drift_penalty: float
    cap_ceil: str


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok", "version": "0.1.0"}


@app.get("/scenarios")
def list_scenarios() -> list[dict[str, Any]]:
    """Return summaries of the bundled example scenarios."""
    here = Path(__file__).resolve().parents[2] / "examples" / "scenarios"
    out: list[dict[str, Any]] = []
    if not here.exists():
        return out
    for p in sorted(here.glob("*.json")):
        try:
            s = Scenario.from_json(str(p))
            out.append({
                "id": s.id,
                "name": s.name,
                "description": s.description[:280],
                "operator_handoff": s.operator_handoff,
                "seed_account_profile": s.seed_account_profile,
            })
        except Exception:
            continue
    return out


@app.post("/score", response_model=ScoreResponse)
def score(run_json: dict[str, Any]) -> ScoreResponse:
    try:
        run = Run.model_validate(run_json)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Invalid Run: {exc}") from exc
    run.reconcile_ledger()
    fc = code_run(run)
    s = boundary_respect_score(fc)
    return ScoreResponse(
        aggregate=s.aggregate,
        honesty=s.honesty,
        handoff=s.handoff,
        refusal_quality=s.refusal_quality,
        drift_penalty=s.drift_penalty,
        cap_ceil=fc.cap_ceil.value,
    )


@app.post("/redact")
def redact(run_json: dict[str, Any], bucket_amounts: bool = True) -> dict[str, Any]:
    try:
        run = Run.model_validate(run_json)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Invalid Run: {exc}") from exc
    redacted = redact_run(run, bucket_amounts=bucket_amounts)
    return redacted.model_dump(mode="json")


@app.post("/adapter/claude_code")
async def adapt_claude_code(
    scenario_id: str,
    agent_id: str = "claude-opus-4-7",
    file: UploadFile = File(...),
) -> dict[str, Any]:
    raw = await file.read()
    with tempfile.NamedTemporaryFile(suffix=".jsonl", delete=False) as tmp:
        tmp.write(raw)
        tmp_path = Path(tmp.name)
    try:
        run = claude_code_transcript_to_run(tmp_path, scenario_id=scenario_id, agent_id=agent_id)
        return run.model_dump(mode="json")
    finally:
        try:
            tmp_path.unlink()
        except OSError:
            pass


@app.post("/adapter/openai_operator")
async def adapt_openai_operator(
    scenario_id: str,
    agent_id: str = "openai-operator",
    file: UploadFile = File(...),
) -> dict[str, Any]:
    raw = await file.read()
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
        tmp.write(raw)
        tmp_path = Path(tmp.name)
    try:
        run = openai_operator_session_to_run(tmp_path, scenario_id=scenario_id, agent_id=agent_id)
        return run.model_dump(mode="json")
    finally:
        try:
            tmp_path.unlink()
        except OSError:
            pass
