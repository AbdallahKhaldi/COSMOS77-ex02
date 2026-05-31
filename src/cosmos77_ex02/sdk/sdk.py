"""The SDK — the single entry point for all business logic (CLAUDE.md rule 2).

The CLI, the terminal menu, the orchestrator entry, and any external consumer
call only :class:`SDK`; they never reach into internal modules. This Phase-2
skeleton wires configuration and stubs the public surface (each method raises
``NotImplementedError`` until its phase lands), so callers can be built and
tested against a stable contract from the start.
"""

from __future__ import annotations

from typing import Any

from cosmos77_ex02.shared.config import Config


class SDK:
    """Programmatic facade over the debate system (config-driven, rule 4)."""

    def __init__(self, config: Config | None = None) -> None:
        self._config = config if config is not None else Config()

    @property
    def config(self) -> Config:
        """The :class:`Config` this SDK was built with."""
        return self._config

    def run_debate(self, topic: str | None = None) -> Any:
        """Run a full debate and return the transcript path + verdict (Phase 6)."""
        raise NotImplementedError("run_debate lands in Phase 6")

    def set_topic(self, topic: str, pro: str | None = None, con: str | None = None) -> None:
        """Update the debate topic and positions in config (Phase 8)."""
        raise NotImplementedError("set_topic lands in Phase 8")

    def set_pings(self, pings_per_side: int) -> None:
        """Update the number of pings per side in config (Phase 8)."""
        raise NotImplementedError("set_pings lands in Phase 8")

    def last_verdict(self) -> Any:
        """Return the verdict from the latest transcript (Phase 7)."""
        raise NotImplementedError("last_verdict lands in Phase 7")

    def cost_report(self) -> Any:
        """Return the token/USD cost report for the latest run (Phase 9)."""
        raise NotImplementedError("cost_report lands in Phase 9")

    def tail_logs(self, n: int = 50) -> list[str]:
        """Return the last ``n`` structured log lines (Phase 8)."""
        raise NotImplementedError("tail_logs lands in Phase 8")

    def build_agent(self, role: str) -> Any:
        """Construct an agent for ``role`` via the factory (rule 2 entry point)."""
        from cosmos77_ex02.agents.factory import build_agent
        from cosmos77_ex02.runtime.claude_cli import ClaudeCliRuntime
        from cosmos77_ex02.shared.gatekeeper import Gatekeeper

        return build_agent(
            role,
            ClaudeCliRuntime(self._config),
            Gatekeeper(self._config.gatekeeper()),
            self._config,
        )
