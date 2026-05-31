"""DebaterAgent — shared Pro/Con turn behaviour (acceptance A4, A7).

A debater's turn rebuts the opponent's last point, advances one new point, and
must cite >=1 web source. Pro and Con differ only by Skill file and the fixed
position string they defend — there is no per-side logic here (rule 3).
"""

from __future__ import annotations

from typing import Any

from cosmos77_ex02.agents.base import BaseAgent
from cosmos77_ex02.agents.prompts import extract_citations, render_turn_prompt
from cosmos77_ex02.protocol.message import ProtocolMessage


class DebaterAgent(BaseAgent):
    """A debater that argues a fixed position with mandatory citations."""

    POSITION_KEY: str = ""

    @property
    def position(self) -> str:
        """The fixed position string this debater defends (from config)."""
        return str(self._config.get(self.POSITION_KEY))

    def act(self, context: dict[str, Any]) -> ProtocolMessage:
        """Build one debate turn and return it as a message addressed to the judge."""
        prompt = render_turn_prompt(self._config, position=self.position, context=context)
        tools = self._config.runtime().get("allowed_tools", [])
        result = self._invoke(prompt, allowed_tools=tools)
        citations = extract_citations(result.text)
        return self._to_message(
            result.text,
            recipient="judge",
            ping_no=int(context.get("ping_no", 1)),
            turn_type=str(context.get("turn_type", "rebuttal")),
            citations=citations,
            result=result,
        )
