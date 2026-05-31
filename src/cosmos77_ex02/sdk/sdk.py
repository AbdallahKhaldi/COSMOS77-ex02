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
        """Run a full debate (3 processes) and return the transcript path + verdict."""
        from cosmos77_ex02.orchestration.orchestrator import Orchestrator

        return Orchestrator(self._config).run()

    def set_topic(self, topic: str, pro: str | None = None, con: str | None = None) -> None:
        """Update the debate topic (and optionally positions) in config and persist."""
        self._config.set("debate.topic", topic)
        if pro is not None:
            self._config.set("debate.pro_position", pro)
        if con is not None:
            self._config.set("debate.con_position", con)
        self._config.save()

    def set_pings(self, pings_per_side: int) -> None:
        """Update the number of pings per side in config and persist."""
        self._config.set("debate.pings_per_side", int(pings_per_side))
        self._config.save()

    def last_verdict(self) -> Any:
        """Return the verdict dict from the most recent transcript, or raise if none."""
        import json
        from pathlib import Path

        directory = Path(self._config.orchestration().get("transcript_dir", "transcripts"))
        sessions = sorted(directory.glob("session_*.json"))
        if not sessions:
            raise FileNotFoundError(f"no transcript found in {directory}; run a debate first")
        data = json.loads(sessions[-1].read_text(encoding="utf-8"))
        return data.get("verdict")

    def cost_report(self) -> Any:
        """Return the token/USD cost report for the latest run (Phase 9)."""
        raise NotImplementedError("cost_report lands in Phase 9")

    def tail_logs(self, n: int = 50) -> list[str]:
        """Return the last ``n`` structured (JSON-lines) log lines across the FIFO files."""
        from pathlib import Path

        logs_dir = Path(self._config.paths().get("logs_dir", "logs"))
        lines: list[str] = []
        for log_file in sorted(logs_dir.glob("*.jsonl")):
            lines.extend(log_file.read_text(encoding="utf-8").splitlines())
        return lines[-n:]

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
