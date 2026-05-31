"""ProtocolMessage envelope: construction, validation, round-trip (A6).

Phase 4 introduces the model; Phase 5 adds routing/serialize/citation tests.
"""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from cosmos77_ex02.protocol.message import ProtocolMessage


def test_create_computes_word_count_and_defaults() -> None:
    m = ProtocolMessage.create(
        sender="pro", recipient="judge", content="one two three", ping_no=1, turn_type="opening"
    )
    assert m.word_count == 3
    assert m.role == "pro"  # defaults to sender
    assert m.msg_id and m.ts  # auto-generated
    assert m.citations == [] and m.tokens == 0 and m.cost_usd == 0.0


def test_invalid_role_rejected() -> None:
    with pytest.raises(ValidationError, match="invalid role"):
        ProtocolMessage.create(
            sender="moderator", recipient="judge", content="x", ping_no=1, turn_type="opening"
        )


def test_invalid_turn_type_rejected() -> None:
    with pytest.raises(ValidationError, match="turn_type"):
        ProtocolMessage.create(
            sender="pro", recipient="judge", content="x", ping_no=1, turn_type="banter"
        )


def test_negative_ping_rejected() -> None:
    with pytest.raises(ValidationError):
        ProtocolMessage.create(
            sender="pro", recipient="judge", content="x", ping_no=-1, turn_type="opening"
        )


def test_round_trips_through_dict() -> None:
    m = ProtocolMessage.create(
        sender="con",
        recipient="judge",
        content="hello world",
        ping_no=2,
        turn_type="rebuttal",
        citations=["https://a.example"],
        msg_id="m1",
        ts="t1",
    )
    again = ProtocolMessage(**m.model_dump())
    assert again == m
    assert again.msg_id == "m1" and again.ts == "t1"
