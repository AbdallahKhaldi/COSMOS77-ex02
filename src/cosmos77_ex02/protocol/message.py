"""The JSON IPC message envelope (pydantic) — every turn child<->judge<->child.

Introduced here because the agents (Phase 4) emit these. Phase 5 adds routing
(:mod:`cosmos77_ex02.protocol.routing`), serialization helpers, and the full
validation suite around this model. Fields follow ``docs/PRD_ipc_protocol.md``.
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, Field, field_validator

from cosmos77_ex02.constants import ROLES, TURN_TYPES


def _new_id() -> str:
    return uuid.uuid4().hex


def _now_iso() -> str:
    return datetime.now(UTC).isoformat()


class ProtocolMessage(BaseModel):
    """One validated, JSON-serialisable debate message."""

    msg_id: str = Field(default_factory=_new_id)
    ts: str = Field(default_factory=_now_iso)
    sender: str
    recipient: str
    role: str
    ping_no: int = Field(ge=0)
    turn_type: str
    content: str
    citations: list[str] = Field(default_factory=list)
    word_count: int = Field(ge=0)
    tokens: int = Field(default=0, ge=0)
    cost_usd: float = Field(default=0.0, ge=0.0)

    @field_validator("sender", "recipient", "role")
    @classmethod
    def _valid_role(cls, value: str) -> str:
        if value not in ROLES:
            raise ValueError(f"invalid role {value!r}; must be one of {ROLES}")
        return value

    @field_validator("turn_type")
    @classmethod
    def _valid_turn_type(cls, value: str) -> str:
        if value not in TURN_TYPES:
            raise ValueError(f"invalid turn_type {value!r}; must be one of {TURN_TYPES}")
        return value

    @classmethod
    def create(
        cls,
        *,
        sender: str,
        recipient: str,
        content: str,
        ping_no: int,
        turn_type: str,
        role: str | None = None,
        citations: list[str] | None = None,
        tokens: int = 0,
        cost_usd: float = 0.0,
        msg_id: str | None = None,
        ts: str | None = None,
    ) -> ProtocolMessage:
        """Build a message, auto-computing ``word_count`` from ``content``."""
        data: dict[str, Any] = {
            "sender": sender,
            "recipient": recipient,
            "role": role if role is not None else sender,
            "content": content,
            "ping_no": ping_no,
            "turn_type": turn_type,
            "citations": list(citations or []),
            "word_count": len(content.split()),
            "tokens": tokens,
            "cost_usd": cost_usd,
        }
        if msg_id is not None:
            data["msg_id"] = msg_id
        if ts is not None:
            data["ts"] = ts
        return cls(**data)
