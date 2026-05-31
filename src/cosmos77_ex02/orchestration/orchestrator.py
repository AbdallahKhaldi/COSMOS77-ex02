"""The Orchestrator — spawns 3 agent processes and runs the working debate.

Owns the transcript (Context Engineering), runs the ping loop with watchdog
supervision, persists ``transcripts/session_NNN.json`` incrementally, and asks
the judge for the final no-tie verdict (acceptance A1, A3, A5, A9). All knobs
come from config. Handles can be injected (for tests); otherwise three real
``AgentProcess`` children are spawned.
"""

from __future__ import annotations

import json
from typing import Any

from cosmos77_ex02.orchestration.loop import run_ping_loop
from cosmos77_ex02.orchestration.process_agent import AgentProcess
from cosmos77_ex02.orchestration.transcript import TranscriptWriter
from cosmos77_ex02.orchestration.watchdog import Watchdog
from cosmos77_ex02.protocol.serialize import to_json
from cosmos77_ex02.shared.logging_setup import get_logger

_ROLES = ("judge", "pro", "con")
_LOG = get_logger("cosmos77_ex02.debate")


class Orchestrator:
    """Runs one full debate across three agent processes to a no-tie verdict."""

    def __init__(
        self,
        config: Any,
        *,
        handles: dict[str, Any] | None = None,
        watchdog: Watchdog | None = None,
        writer: TranscriptWriter | None = None,
    ) -> None:
        self._config = config
        self._handles = handles
        orchestration = config.orchestration()
        self._watchdog = watchdog or Watchdog(
            keepalive_seconds=float(orchestration.get("watchdog_keepalive_seconds", 15)),
            max_restarts=int(orchestration.get("max_restarts_per_agent", 3)),
        )
        self._writer = writer

    def run(self) -> dict[str, Any]:
        """Spawn the agents, run the loop, append the verdict, and return a summary."""
        handles = self._handles or self._spawn_handles()
        for handle in handles.values():
            if not handle.alive:
                handle.start()
        writer = self._writer or TranscriptWriter(
            self._config.orchestration().get("transcript_dir", "transcripts")
        )
        pings = int(self._config.get("debate.pings_per_side", 10))
        timeout = float(self._config.runtime().get("per_call_timeout_seconds", 120))
        transcript: list[Any] = []
        meta = self._meta()

        def _on_message(message: Any) -> None:
            _LOG.info(to_json(message))  # structured FIFO log line (no-op if logging unconfigured)
            writer.write(meta, transcript)

        try:
            _LOG.info(json.dumps({"event": "debate_start", "topic": meta.get("topic", "")}))
            run_ping_loop(
                handles,
                pings=pings,
                per_call_timeout=timeout,
                watchdog=self._watchdog,
                transcript=transcript,
                on_message=_on_message,
            )
            verdict = self._watchdog.guarded_call(
                handles["judge"], "verdict", timeout, transcript=transcript
            )
            _LOG.info(json.dumps({"event": "verdict", "winner": verdict.winner}))
            path = writer.write(meta, transcript, verdict=verdict)
        finally:
            if self._handles is None:
                for handle in handles.values():
                    handle.terminate()
        return {"transcript_path": str(path), "verdict": verdict, "messages": len(transcript)}

    def _spawn_handles(self) -> dict[str, AgentProcess]:
        config_dir = str(self._config.config_dir)
        return {role: AgentProcess(role, config_dir=config_dir) for role in _ROLES}

    def _meta(self) -> dict[str, Any]:
        debate = self._config.debate()
        return {
            "topic": debate.get("topic", ""),
            "pro_position": debate.get("pro_position", ""),
            "con_position": debate.get("con_position", ""),
            "pings_per_side": int(self._config.get("debate.pings_per_side", 10)),
        }
