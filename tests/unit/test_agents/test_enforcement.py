"""Judge enforcement helpers: rebuttal + anti-collusion detection (A4, A10)."""

from __future__ import annotations

from cosmos77_ex02.agents.enforcement import (
    detect_agreement_drift,
    enforcement_problems,
    references_opponent,
)
from cosmos77_ex02.protocol.message import ProtocolMessage
from cosmos77_ex02.shared.config import Config


def _turn(content: str, citations: list[str]) -> ProtocolMessage:
    return ProtocolMessage.create(
        sender="pro",
        recipient="judge",
        content=content,
        ping_no=2,
        turn_type="rebuttal",
        citations=citations,
    )


def test_detect_agreement_drift_true() -> None:
    assert detect_agreement_drift("Honestly, I agree with you on this.") is True
    assert detect_agreement_drift("I concede the point entirely.") is True


def test_detect_agreement_drift_false() -> None:
    assert detect_agreement_drift("I strongly disagree and here is why.") is False


def test_references_opponent_via_cue() -> None:
    assert references_opponent("However, your point ignores scale.", "anything") is True


def test_references_opponent_via_keyword_overlap() -> None:
    opp = "Social media harms adolescent mental health through addictive design."
    turn = "Adolescent mental health improves with supportive online communities."
    assert references_opponent(turn, opp) is True


def test_references_opponent_false_when_unrelated() -> None:
    opp = "Social media harms adolescent mental health badly."
    turn = "Quarterly economic output rose three percent globally."
    assert references_opponent(turn, opp) is False


def test_opening_turn_needs_no_rebuttal() -> None:
    assert references_opponent("My opening case.", None) is True


def test_enforcement_problems_flags_non_rebuttal() -> None:
    msg = _turn("Quarterly economic output rose globally.", ["https://a.example"])
    problems = enforcement_problems(msg, Config(), opponent_last="Mental health harm from apps.")
    assert any("no rebuttal" in p for p in problems)


def test_enforcement_problems_flags_agreement_drift() -> None:
    msg = _turn("I agree with you completely. https://a.example", ["https://a.example"])
    problems = enforcement_problems(msg, Config(), opponent_last="Apps harm teens.")
    assert any("agreement drift" in p for p in problems)


def test_enforcement_problems_clean_turn() -> None:
    msg = _turn("However, your claim about harm ignores access benefits.", ["https://a.example"])
    assert enforcement_problems(msg, Config(), opponent_last="Apps harm teens.") == []
