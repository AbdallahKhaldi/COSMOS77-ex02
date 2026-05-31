"""The ping loop + per-turn context construction (acceptance A3, A4, A5).

A "ping" is one Pro turn followed by one Con turn; each turn is routed through
the judge (child -> judge -> child). Each turn's context carries the opponent's
last argument plus a running summary (Context Engineering), and every produced
message is route-validated and persisted via ``on_message``.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from cosmos77_ex02.orchestration.summary import running_summary
from cosmos77_ex02.protocol.routing import validate_route


def turn_type(ping_no: int, total: int) -> str:
    """Classify a turn: opening (first ping), closing (last), else rebuttal."""
    if ping_no == 1:
        return "opening"
    if ping_no >= total:
        return "closing"
    return "rebuttal"


def build_context(
    transcript: list[Any], *, ping_no: int, total: int, opponent_last: str | None
) -> dict[str, Any]:
    """Select the opponent's last turn + a running summary into the next prompt."""
    context: dict[str, Any] = {
        "ping_no": ping_no,
        "turn_type": turn_type(ping_no, total),
        "summary": running_summary(transcript),
    }
    if opponent_last is not None:
        context["opponent_last"] = opponent_last
    return context


def run_ping_loop(
    handles: dict[str, Any],
    *,
    pings: int,
    per_call_timeout: float,
    watchdog: Any,
    transcript: list[Any],
    on_message: Callable[[Any], None],
) -> list[Any]:
    """Run ``pings`` rounds of Pro->judge->Con->judge, returning the transcript."""
    judge = handles["judge"]
    last: dict[str, str | None] = {"pro": None, "con": None}
    for ping in range(1, pings + 1):
        for side, other in (("pro", "con"), ("con", "pro")):
            context = build_context(
                transcript, ping_no=ping, total=pings, opponent_last=last[other]
            )
            message = watchdog.guarded_call(handles[side], "act", per_call_timeout, context=context)
            validate_route(message.sender, message.recipient)
            transcript.append(message)
            on_message(message)
            relayed = watchdog.guarded_call(
                judge, "relay", per_call_timeout, message=message, recipient=other
            )
            validate_route(relayed.sender, relayed.recipient)
            transcript.append(relayed)
            on_message(relayed)
            last[side] = message.content
    return transcript
