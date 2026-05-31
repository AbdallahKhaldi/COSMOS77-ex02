"""Watchdog — per-call timeouts + kill/restart of stalled or dead agents (A11).

Wraps every agent call: if the target process is dead it is restarted before the
call; if the call stalls past its timeout (``RuntimeTimeout``), the process is
terminated and restarted and the *same* request is replayed, up to
``max_restarts`` per agent. When restarts are exhausted the error propagates so
the debate fails loudly rather than hanging.
"""

from __future__ import annotations

from typing import Any

from cosmos77_ex02.runtime.claude_cli import RuntimeTimeout
from cosmos77_ex02.shared.logging_setup import get_logger

_LOG = get_logger("cosmos77_ex02.watchdog")


class Watchdog:
    """Supervises agent handles: detects stalls/deaths and restarts them."""

    def __init__(self, keepalive_seconds: float = 15.0, max_restarts: int = 3) -> None:
        self.keepalive_seconds = keepalive_seconds
        self.max_restarts = max_restarts
        self._restarts: dict[str, int] = {}

    def restarts_for(self, role: str) -> int:
        """How many times ``role`` has been restarted so far."""
        return self._restarts.get(role, 0)

    def is_stalled(self, handle: Any) -> bool:
        """True if the handle is dead or its heartbeat is older than the keepalive."""
        return (not handle.alive) or handle.heartbeat_age() > self.keepalive_seconds

    def guarded_call(self, handle: Any, method: str, timeout: float, **kwargs: Any) -> Any:
        """Call ``handle.method(**kwargs)``, restarting + replaying on stall/death."""
        while True:
            if not handle.alive and not self._restart(handle):
                raise RuntimeError(f"{handle.role} is dead and restarts are exhausted")
            try:
                return handle.call(method, timeout=timeout, **kwargs)
            except RuntimeTimeout:
                _LOG.warning("%s.%s stalled; restarting and replaying", handle.role, method)
                if not self._restart(handle):
                    raise

    def _restart(self, handle: Any) -> bool:
        """Restart ``handle`` if it has budget left; return False when exhausted."""
        used = self._restarts.get(handle.role, 0)
        if used >= self.max_restarts:
            _LOG.error("%s exhausted its %d restarts", handle.role, self.max_restarts)
            return False
        self._restarts[handle.role] = used + 1
        handle.restart()
        _LOG.info("restarted %s (%d/%d)", handle.role, used + 1, self.max_restarts)
        return True
