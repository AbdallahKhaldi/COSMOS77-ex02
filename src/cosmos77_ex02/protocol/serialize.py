"""UTF-8 JSON (de)serialization for protocol messages (acceptance A6).

Thin wrappers over pydantic so the orchestrator and the FIFO logs persist and
reload messages through one place; transcripts are JSON-lines (one message per
line) for easy auditing.
"""

from __future__ import annotations

from collections.abc import Iterable

from cosmos77_ex02.protocol.message import ProtocolMessage


def to_json(message: ProtocolMessage) -> str:
    """Serialize a message to a compact JSON string (UTF-8, English)."""
    return message.model_dump_json()


def from_json(text: str) -> ProtocolMessage:
    """Parse a JSON string back into a validated :class:`ProtocolMessage`."""
    return ProtocolMessage.model_validate_json(text)


def to_jsonl(messages: Iterable[ProtocolMessage]) -> str:
    """Serialize messages to JSON-lines (one message per line)."""
    return "\n".join(to_json(m) for m in messages)


def from_jsonl(text: str) -> list[ProtocolMessage]:
    """Parse JSON-lines back into a list of messages (blank lines ignored)."""
    return [from_json(line) for line in text.splitlines() if line.strip()]
