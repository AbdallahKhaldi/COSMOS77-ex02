"""Verdict invariants: never a tie, winner == higher score, justification required."""

from __future__ import annotations

import pytest

from cosmos77_ex02.agents.verdict import Verdict


def test_valid_verdict_round_trips() -> None:
    v = Verdict("pro", 80, 73, "Pro was clearer.", "2026-05-31T00:00:00+00:00")
    assert v.to_dict()["winner"] == "pro"
    assert v.to_dict()["pro_score"] == 80


def test_tie_is_rejected() -> None:
    with pytest.raises(ValueError, match="tie"):
        Verdict("pro", 75, 75, "even", "t")


def test_winner_must_have_higher_score() -> None:
    with pytest.raises(ValueError, match="higher score"):
        Verdict("con", 80, 73, "inconsistent", "t")


def test_empty_justification_rejected() -> None:
    with pytest.raises(ValueError, match="justification"):
        Verdict("pro", 80, 73, "   ", "t")


def test_invalid_winner_rejected() -> None:
    with pytest.raises(ValueError, match="winner"):
        Verdict("draw", 80, 73, "x", "t")
