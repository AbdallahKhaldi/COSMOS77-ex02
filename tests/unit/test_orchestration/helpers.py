"""Module-level test doubles for the orchestration layer.

Defined at module level (not in conftest) so they are importable by qualified
name and therefore picklable by the ``spawn`` start method used in the real
AgentProcess test. No real ``claude`` is ever invoked.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from cosmos77_ex02.agents.verdict import Verdict
from cosmos77_ex02.protocol.message import ProtocolMessage
from cosmos77_ex02.runtime.claude_cli import RuntimeTimeout


class FakeHandle:
    """In-process stand-in for AgentProcess (no real process)."""

    def __init__(self, role: str, responder: Callable[[str, dict], Any]) -> None:
        self.role = role
        self._responder = responder
        self.alive = False
        self.restarts = 0
        self.calls: list[tuple[str, dict]] = []

    def start(self) -> None:
        self.alive = True

    def terminate(self) -> None:
        self.alive = False

    def restart(self) -> None:
        self.restarts += 1
        self.alive = True

    def heartbeat_age(self) -> float:
        return 0.0

    def call(self, method: str, *, timeout: float | None = None, **kwargs: Any) -> Any:
        self.calls.append((method, kwargs))
        return self._responder(method, kwargs)


def debater_responder(role: str) -> Callable[[str, dict], ProtocolMessage]:
    """A responder that returns a canned, well-formed debater turn."""

    def respond(method: str, kwargs: dict) -> ProtocolMessage:
        ctx = kwargs.get("context", {})
        return ProtocolMessage.create(
            sender=role,
            recipient="judge",
            content=f"{role} argues with evidence. Sources: https://example.com/{role}",
            ping_no=int(ctx.get("ping_no", 1)),
            turn_type=str(ctx.get("turn_type", "rebuttal")),
            citations=[f"https://example.com/{role}"],
        )

    return respond


def judge_responder() -> Callable[[str, dict], Any]:
    """A responder that relays messages and returns a no-tie verdict."""

    def respond(method: str, kwargs: dict) -> Any:
        if method == "relay":
            msg = kwargs["message"]
            return ProtocolMessage.create(
                sender="judge",
                recipient=kwargs["recipient"],
                content=msg.content,
                ping_no=msg.ping_no,
                turn_type=msg.turn_type,
                citations=list(msg.citations),
            )
        if method == "verdict":
            return Verdict("pro", 80, 73, "Pro rebutted more sharply.", "2026-05-31T00:00:00+00:00")
        raise ValueError(f"unexpected judge method {method!r}")

    return respond


class FlakyResponder:
    """Raises RuntimeTimeout the first ``fail_times`` calls, then succeeds."""

    def __init__(self, fail_times: int) -> None:
        self.fail_times = fail_times
        self.attempts = 0

    def __call__(self, method: str, kwargs: dict) -> str:
        self.attempts += 1
        if self.attempts <= self.fail_times:
            raise RuntimeTimeout("simulated stall")
        return "ok"


class FakeAgent:
    """A picklable agent with no LLM, for the real-process AgentProcess test."""

    def __init__(self, role: str) -> None:
        self.role = role

    def act(self, context: dict) -> ProtocolMessage:
        return ProtocolMessage.create(
            sender=self.role,
            recipient="judge",
            content=f"{self.role} canned turn. Sources: https://example.com/x",
            ping_no=int(context.get("ping_no", 1)),
            turn_type=str(context.get("turn_type", "opening")),
            citations=["https://example.com/x"],
        )


def build_fake_agent(role: str, config_dir: str | None) -> FakeAgent:
    """Module-level builder so it is picklable for the spawn start method."""
    return FakeAgent(role)
