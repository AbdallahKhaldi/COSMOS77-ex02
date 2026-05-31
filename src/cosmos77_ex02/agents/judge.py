"""JudgeAgent — the father: routes, enforces turn rules, and renders a verdict.

Phase 4 establishes routing, basic enforcement, a starter scoring rubric, and an
LLM-driven no-tie verdict. Phase 7 strengthens enforcement (rebuttal/agreement
detection) and the persuasion rubric. The judge never knows the "right answer".
"""

from __future__ import annotations

import json
import re
from datetime import UTC, datetime
from typing import Any

from cosmos77_ex02.agents.base import BaseAgent
from cosmos77_ex02.agents.prompts import render_verdict_prompt
from cosmos77_ex02.agents.verdict import Verdict
from cosmos77_ex02.protocol.message import ProtocolMessage

_JSON_RE = re.compile(r"\{.*\}", re.DOTALL)


class JudgeAgent(BaseAgent):
    """Routes child<->child, enforces the rules, and decides a no-tie winner."""

    ROLE = "judge"
    SKILL_FILE = "skill_judge.md"

    def act(self, context: dict[str, Any]) -> ProtocolMessage:
        """Relay the incoming child message toward the other child."""
        return self.relay(context["message"], context["recipient"], context.get("note"))

    def relay(
        self, message: ProtocolMessage, recipient: str, note: str | None = None
    ) -> ProtocolMessage:
        """Forward a child's message to the opponent (optionally with a note)."""
        content = message.content if not note else f"[Judge note: {note}]\n{message.content}"
        return ProtocolMessage.create(
            sender="judge",
            recipient=recipient,
            role="judge",
            content=content,
            ping_no=message.ping_no,
            turn_type=message.turn_type,
            citations=list(message.citations),
        )

    def enforce(self, message: ProtocolMessage, config: Any | None = None) -> list[str]:
        """Return the list of rule violations for ``message`` (empty if clean)."""
        debate = (config or self._config).debate()
        problems: list[str] = []
        if debate.get("require_citation_per_turn", True) and not message.citations:
            problems.append("missing citation: each debater turn must cite >=1 web source")
        max_words = int(debate.get("max_words_per_turn", 180))
        if message.word_count > max_words:
            problems.append(f"over word limit: {message.word_count} > {max_words}")
        return problems

    def score_turn(self, message: ProtocolMessage) -> dict[str, int]:
        """Starter persuasion rubric (Phase 7 replaces with an LLM-scored rubric)."""
        return {
            "clarity": min(10, max(1, message.word_count // 20)),
            "evidence": min(10, len(message.citations) * 3),
            "rebuttal": 5,
            "rhetoric": 5,
        }

    def verdict(self, transcript: list[ProtocolMessage]) -> Verdict:
        """Ask the LLM judge for a verdict, enforce no-tie, and return it."""
        result = self._invoke(render_verdict_prompt(self._config, transcript), allowed_tools=[])
        data = self._parse_verdict(result.text)
        pro = int(data.get("pro_score", 0))
        con = int(data.get("con_score", 0))
        winner = str(data.get("winner", "")).lower()
        justification = str(data.get("justification", "")).strip() or "No justification provided."
        pro, con, winner = _resolve_winner(pro, con, winner)
        return Verdict(
            winner=winner,
            pro_score=pro,
            con_score=con,
            justification=justification,
            decided_at=datetime.now(UTC).isoformat(),
        )

    @staticmethod
    def _parse_verdict(text: str) -> dict[str, Any]:
        match = _JSON_RE.search(text)
        if not match:
            raise ValueError("judge returned no JSON verdict object")
        return json.loads(match.group(0))


def _resolve_winner(pro: int, con: int, winner: str) -> tuple[int, int, str]:
    """Guarantee a strict winner (no tie); trust the higher score for consistency."""
    if pro == con:
        chosen = winner if winner in ("pro", "con") else "pro"
        if chosen == "pro":
            pro += 1
        else:
            con += 1
        return pro, con, chosen
    return pro, con, ("pro" if pro > con else "con")
