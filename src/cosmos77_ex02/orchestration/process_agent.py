"""Run ONE agent in its own OS process over multiprocessing Queues (A1).

Each debate agent (judge / pro / con) is a separate process. The parent sends
``{method, kwargs}`` requests on an inbound queue; the child builds the agent
*inside itself* (so the runtime/gatekeeper are never pickled), dispatches the
method, and returns the result on the outbound queue while bumping a shared
heartbeat the Watchdog reads. The child is built fresh on restart.
"""

from __future__ import annotations

import multiprocessing as mp
import time
from queue import Empty
from typing import Any

from cosmos77_ex02.runtime.claude_cli import RuntimeTimeout

_STOP = "__STOP__"


def build_default_agent(role: str, config_dir: str | None) -> Any:
    """Construct a production agent inside the child process."""
    from cosmos77_ex02.agents.factory import build_agent
    from cosmos77_ex02.runtime.claude_cli import ClaudeCliRuntime
    from cosmos77_ex02.shared.config import Config
    from cosmos77_ex02.shared.gatekeeper import Gatekeeper

    cfg = Config(config_dir) if config_dir else Config()
    return build_agent(role, ClaudeCliRuntime(cfg), Gatekeeper(cfg.gatekeeper()), cfg)


def _worker(role, config_dir, builder, inbound, outbound, heartbeat) -> None:  # noqa: ANN001
    """Child entry point: build the agent, then serve requests until stopped."""
    agent = (builder or build_default_agent)(role, config_dir)
    heartbeat.value = time.time()
    while True:
        request = inbound.get()
        if request == _STOP:
            break
        heartbeat.value = time.time()
        try:
            result = getattr(agent, request["method"])(**request.get("kwargs", {}))
            outbound.put({"ok": True, "result": result})
        except Exception as exc:  # report; keep the process alive for the next request
            outbound.put({"ok": False, "error": f"{type(exc).__name__}: {exc}"})
        heartbeat.value = time.time()


class AgentProcess:
    """A handle to one agent running in its own process."""

    def __init__(self, role: str, config_dir: str | None = None, agent_builder: Any = None) -> None:
        self.role = role
        self._config_dir = config_dir
        self._builder = agent_builder
        self._ctx = mp.get_context("spawn")
        self._proc: Any = None
        self._inbound: Any = None
        self._outbound: Any = None
        self._heartbeat: Any = None

    def start(self) -> None:
        """Spawn the child process and its queues."""
        self._inbound = self._ctx.Queue()
        self._outbound = self._ctx.Queue()
        self._heartbeat = self._ctx.Value("d", 0.0)
        self._proc = self._ctx.Process(
            target=_worker,
            args=(
                self.role,
                self._config_dir,
                self._builder,
                self._inbound,
                self._outbound,
                self._heartbeat,
            ),
            daemon=True,
        )
        self._proc.start()

    @property
    def alive(self) -> bool:
        return self._proc is not None and self._proc.is_alive()

    def heartbeat_age(self) -> float:
        """Seconds since the child last reported progress (inf if never started)."""
        if self._heartbeat is None or self._heartbeat.value == 0.0:
            return float("inf")
        return time.time() - self._heartbeat.value

    def call(self, method: str, *, timeout: float | None = None, **kwargs: Any) -> Any:
        """Send a request to the child and wait for its result (RuntimeTimeout on stall)."""
        self._inbound.put({"method": method, "kwargs": kwargs})
        try:
            response = self._outbound.get(timeout=timeout)
        except Empty as exc:
            raise RuntimeTimeout(f"{self.role}.{method} exceeded {timeout}s") from exc
        if not response["ok"]:
            raise RuntimeError(f"{self.role}.{method} failed: {response['error']}")
        return response["result"]

    def terminate(self) -> None:
        """Stop the child process."""
        if self._proc is not None and self._proc.is_alive():
            self._proc.terminate()
            self._proc.join(timeout=5)

    def restart(self) -> None:
        """Terminate and re-spawn a fresh child (state is rebuilt from config)."""
        self.terminate()
        self.start()
