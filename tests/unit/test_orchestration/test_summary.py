"""Running-summary builder (Context Engineering)."""

from __future__ import annotations

from cosmos77_ex02.orchestration.summary import running_summary
from cosmos77_ex02.protocol.message import ProtocolMessage


def _msg(sender: str, content: str, ping: int) -> ProtocolMessage:
    return ProtocolMessage.create(
        sender=sender, recipient="judge", content=content, ping_no=ping, turn_type="rebuttal"
    )


def test_summary_includes_recent_debater_turns() -> None:
    transcript = [_msg("pro", "Pro point one. Extra.", 1), _msg("con", "Con point one. Extra.", 1)]
    summary = running_summary(transcript)
    assert "pro (ping 1)" in summary and "con (ping 1)" in summary
    assert "Pro point one" in summary


def test_summary_excludes_judge_relays() -> None:
    transcript = [_msg("judge", "relayed text here", 1)]
    assert running_summary(transcript) == ""


def test_summary_is_length_bounded() -> None:
    transcript = [_msg("pro", "x " * 500, i) for i in range(1, 10)]
    assert len(running_summary(transcript, max_chars=200)) <= 200
