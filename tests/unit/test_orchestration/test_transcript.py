"""TranscriptWriter: incremental session JSON + verdict."""

from __future__ import annotations

import json
from pathlib import Path

from cosmos77_ex02.agents.verdict import Verdict
from cosmos77_ex02.orchestration.transcript import TranscriptWriter
from cosmos77_ex02.protocol.message import ProtocolMessage


def _msg() -> ProtocolMessage:
    return ProtocolMessage.create(
        sender="pro", recipient="judge", content="hi", ping_no=1, turn_type="opening"
    )


def test_writes_session_file_with_messages(tmp_path: Path) -> None:
    writer = TranscriptWriter(tmp_path, session_no=1)
    path = writer.write({"topic": "T"}, [_msg()])
    assert path.name == "session_001.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["topic"] == "T"
    assert len(data["messages"]) == 1
    assert data["verdict"] is None


def test_writes_verdict_when_provided(tmp_path: Path) -> None:
    writer = TranscriptWriter(tmp_path, session_no=2)
    verdict = Verdict("pro", 80, 73, "because", "t")
    data = json.loads(writer.write({}, [_msg()], verdict=verdict).read_text(encoding="utf-8"))
    assert data["verdict"]["winner"] == "pro"


def test_next_session_no_increments(tmp_path: Path) -> None:
    (tmp_path / "session_001.json").write_text("{}")
    (tmp_path / "session_004.json").write_text("{}")
    assert TranscriptWriter(tmp_path).session_no == 5


def test_first_session_is_one(tmp_path: Path) -> None:
    assert TranscriptWriter(tmp_path).session_no == 1
