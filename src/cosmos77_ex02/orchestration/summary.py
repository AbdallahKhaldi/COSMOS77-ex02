"""Running-summary builder for Context Engineering (PRD_orchestrator).

The orchestrator hands each agent only the opponent's last turn plus a short
running summary of earlier turns, so prompts stay small and cheap (Select +
Write/evict). This module produces that summary from the transcript so far.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from cosmos77_ex02.protocol.message import ProtocolMessage

_CHILDREN = ("pro", "con")


def running_summary(
    transcript: list[ProtocolMessage], *, recent_turns: int = 6, max_chars: int = 700
) -> str:
    """Condense the recent debater turns into a compact one-line summary."""
    parts: list[str] = []
    for message in transcript[-recent_turns:]:
        if message.sender in _CHILDREN:
            snippet = message.content.strip().replace("\n", " ").split(". ")[0]
            parts.append(f"{message.sender} (ping {message.ping_no}): {snippet[:140]}")
    return " | ".join(parts)[:max_chars]
