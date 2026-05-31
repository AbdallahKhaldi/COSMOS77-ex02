"""Agent factory — ``build_agent(role, ...)`` (extension point, ADR / PRD_extension_points).

Adding a new agent type means subclassing :class:`BaseAgent` and registering it
here; no caller changes. Unknown roles raise rather than silently misbehave.
"""

from __future__ import annotations

from typing import Any

from cosmos77_ex02.agents.base import BaseAgent
from cosmos77_ex02.agents.con import ConAgent
from cosmos77_ex02.agents.judge import JudgeAgent
from cosmos77_ex02.agents.pro import ProAgent

_REGISTRY: dict[str, type[BaseAgent]] = {
    "pro": ProAgent,
    "con": ConAgent,
    "judge": JudgeAgent,
}


def build_agent(
    role: str,
    runtime: Any,
    gatekeeper: Any,
    config: Any,
    *,
    skill_text: str | None = None,
) -> BaseAgent:
    """Construct the agent for ``role``; raise ``ValueError`` for unknown roles."""
    try:
        cls = _REGISTRY[role]
    except KeyError:
        raise ValueError(f"unknown role {role!r}; expected one of {sorted(_REGISTRY)}") from None
    return cls(runtime, gatekeeper, config, skill_text=skill_text)
