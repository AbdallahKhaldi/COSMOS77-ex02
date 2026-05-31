"""Messages round-trip through JSON / JSON-lines (A6)."""

from __future__ import annotations

import pytest

from cosmos77_ex02.protocol.message import ProtocolMessage
from cosmos77_ex02.protocol.serialize import from_json, from_jsonl, to_json, to_jsonl


def _msg(sender: str = "pro", content: str = "hello world") -> ProtocolMessage:
    return ProtocolMessage.create(
        sender=sender,
        recipient="judge",
        content=content,
        ping_no=1,
        turn_type="opening",
        citations=["https://a.example"],
        msg_id="m",
        ts="t",
    )


def test_json_round_trip_is_lossless() -> None:
    m = _msg()
    assert from_json(to_json(m)) == m


def test_to_json_is_valid_json_string() -> None:
    text = to_json(_msg())
    assert text.startswith("{") and '"sender":"pro"' in text.replace(" ", "")


def test_from_json_rejects_invalid_payload() -> None:
    with pytest.raises(ValueError):
        from_json('{"sender": "alien"}')  # missing fields + invalid role


def test_jsonl_round_trip() -> None:
    msgs = [_msg("pro", "a"), _msg("con", "b")]
    text = to_jsonl(msgs)
    assert text.count("\n") == 1
    assert from_jsonl(text) == msgs


def test_from_jsonl_ignores_blank_lines() -> None:
    text = to_json(_msg()) + "\n\n"
    assert len(from_jsonl(text)) == 1
