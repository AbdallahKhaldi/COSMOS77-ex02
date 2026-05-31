"""Orchestrator loop with in-process fake handles (no real processes, no LLM)."""

from __future__ import annotations

import json
from pathlib import Path

from cosmos77_ex02.agents.verdict import Verdict
from cosmos77_ex02.orchestration.orchestrator import Orchestrator
from cosmos77_ex02.orchestration.transcript import TranscriptWriter
from cosmos77_ex02.protocol.routing import is_through_father
from cosmos77_ex02.shared.config import Config
from tests.unit.test_orchestration.helpers import (
    FakeHandle,
    debater_responder,
    judge_responder,
)


def _handles() -> dict[str, FakeHandle]:
    return {
        "judge": FakeHandle("judge", judge_responder()),
        "pro": FakeHandle("pro", debater_responder("pro")),
        "con": FakeHandle("con", debater_responder("con")),
    }


def _run(tmp_path: Path) -> dict:
    cfg = Config()
    writer = TranscriptWriter(tmp_path, session_no=1)
    out = Orchestrator(cfg, handles=_handles(), writer=writer).run()
    out["_pings"] = cfg.get("debate.pings_per_side")
    return out


def test_loop_produces_exactly_pings_per_side(tmp_path: Path) -> None:
    out = _run(tmp_path)
    data = json.loads((tmp_path / "session_001.json").read_text(encoding="utf-8"))
    msgs = data["messages"]
    pro = [m for m in msgs if m["sender"] == "pro"]
    con = [m for m in msgs if m["sender"] == "con"]
    assert len(pro) == out["_pings"]
    assert len(con) == out["_pings"]


def test_every_message_routed_through_judge(tmp_path: Path) -> None:
    data = json.loads(Path(_run(tmp_path)["transcript_path"]).read_text(encoding="utf-8"))
    pairs = [(m["sender"], m["recipient"]) for m in data["messages"]]
    assert is_through_father(pairs)  # no direct child -> child hop


def test_verdict_is_no_tie_and_persisted(tmp_path: Path) -> None:
    out = _run(tmp_path)
    assert isinstance(out["verdict"], Verdict)
    assert out["verdict"].pro_score != out["verdict"].con_score
    data = json.loads((tmp_path / "session_001.json").read_text(encoding="utf-8"))
    assert data["verdict"]["winner"] in ("pro", "con")
    assert data["topic"]


def test_transcript_has_four_messages_per_ping(tmp_path: Path) -> None:
    out = _run(tmp_path)
    assert out["messages"] == out["_pings"] * 4  # pro + judge + con + judge each ping


def test_spawn_handles_creates_three_agent_processes() -> None:
    from cosmos77_ex02.orchestration.process_agent import AgentProcess

    handles = Orchestrator(Config())._spawn_handles()  # constructs, does not start
    assert set(handles) == {"judge", "pro", "con"}
    assert all(isinstance(h, AgentProcess) for h in handles.values())
    assert all(not h.alive for h in handles.values())
