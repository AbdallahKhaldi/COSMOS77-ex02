"""Incremental session transcript writer (PRD_orchestrator, acceptance A15).

Persists ``transcripts/session_NNN.json`` after every turn so a crash leaves a
partial-but-valid transcript, and writes the final verdict at the end. The JSON
is the graded artifact the README embeds and the grader audits.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from cosmos77_ex02.agents.verdict import Verdict
    from cosmos77_ex02.protocol.message import ProtocolMessage


class TranscriptWriter:
    """Writes a single debate session to ``<directory>/session_NNN.json``."""

    def __init__(self, directory: str | Path, session_no: int | None = None) -> None:
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)
        self.session_no = session_no if session_no is not None else self._next_session_no()
        self.path = self.directory / f"session_{self.session_no:03d}.json"

    def _next_session_no(self) -> int:
        existing = sorted(self.directory.glob("session_*.json"))
        numbers = []
        for item in existing:
            tail = item.stem.rsplit("_", 1)[-1]
            if tail.isdigit():
                numbers.append(int(tail))
        return (max(numbers) + 1) if numbers else 1

    def write(
        self,
        meta: dict[str, Any],
        messages: list[ProtocolMessage],
        verdict: Verdict | None = None,
    ) -> Path:
        """Write the full session (metadata + messages + verdict) to disk."""
        data: dict[str, Any] = {
            **meta,
            "messages": [m.model_dump() for m in messages],
            "verdict": verdict.to_dict() if verdict is not None else None,
        }
        self.path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        return self.path
