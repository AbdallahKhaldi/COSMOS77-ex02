"""BaseAgent — the shared agent abstraction over the claude -p runtime.

Holds the role, the loaded Skill text, the runtime, the Gatekeeper, and the
config. Subclasses implement :meth:`act`; everything common (skill loading,
metered invocation, message construction) lives here so there is no duplication
across Pro/Con/Judge (CLAUDE.md rule 3). Every LLM call goes through
``Gatekeeper.guard`` (rule 13).
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import Any

from cosmos77_ex02.agents.prompts import load_skill
from cosmos77_ex02.protocol.message import ProtocolMessage
from cosmos77_ex02.runtime.parse import LlmResult


class BaseAgent(ABC):
    """Abstract base for every debate agent."""

    ROLE: str = ""
    SKILL_FILE: str = ""

    def __init__(
        self,
        runtime: Any,
        gatekeeper: Any,
        config: Any,
        *,
        skill_text: str | None = None,
    ) -> None:
        self._runtime = runtime
        self._gatekeeper = gatekeeper
        self._config = config
        self._skill = skill_text if skill_text is not None else load_skill(self.SKILL_FILE)

    @property
    def role(self) -> str:
        """The agent's role (``judge`` / ``pro`` / ``con``)."""
        return self.ROLE

    @property
    def skill(self) -> str:
        """The loaded Skill prompt text driving this agent's persona."""
        return self._skill

    @abstractmethod
    def act(self, context: dict[str, Any]) -> ProtocolMessage:
        """Produce this agent's next protocol message from ``context``."""

    def _invoke(self, user_prompt: str, *, allowed_tools: Sequence[str] | None = None) -> LlmResult:
        """Run one metered LLM call (Skill as system prompt) via the Gatekeeper."""
        return self._gatekeeper.guard(
            lambda: self._runtime.invoke(self._skill, user_prompt, allowed_tools=allowed_tools)
        )

    def _to_message(
        self,
        text: str,
        *,
        recipient: str,
        ping_no: int,
        turn_type: str,
        citations: list[str],
        result: LlmResult,
    ) -> ProtocolMessage:
        """Wrap an LLM result into a validated :class:`ProtocolMessage`."""
        return ProtocolMessage.create(
            sender=self.ROLE,
            recipient=recipient,
            role=self.ROLE,
            content=text,
            ping_no=ping_no,
            turn_type=turn_type,
            citations=citations,
            tokens=result.input_tokens + result.output_tokens,
            cost_usd=result.cost_usd,
        )
