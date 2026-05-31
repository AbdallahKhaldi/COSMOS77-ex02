"""Tests for the core domain constants (Phase 0 smoke + value contract).

This is the first test in the suite: it proves the package imports cleanly,
exercises the only Phase-0 module that carries executable code, and pins the
role/turn vocabulary that every later phase depends on.
"""

from __future__ import annotations

from cosmos77_ex02 import constants


def test_roles_are_the_three_expected_agents() -> None:
    """ROLES must be exactly judge, pro, con — the three-process cast (A1)."""
    assert constants.ROLES == ("judge", "pro", "con")


def test_turn_types_cover_the_debate_phases() -> None:
    """TURN_TYPES must enumerate opening, rebuttal, closing in order."""
    assert constants.TURN_TYPES == ("opening", "rebuttal", "closing")


def test_default_encoding_is_utf8() -> None:
    """All I/O standardizes on UTF-8 for English-only output."""
    assert constants.DEFAULT_ENCODING == "utf-8"


def test_constants_are_immutable_tuples() -> None:
    """ROLES and TURN_TYPES are tuples so they cannot be mutated at runtime."""
    assert isinstance(constants.ROLES, tuple)
    assert isinstance(constants.TURN_TYPES, tuple)


def test_roles_and_turn_types_have_no_duplicates() -> None:
    """Each vocabulary is a set of distinct values (no accidental repeats)."""
    assert len(set(constants.ROLES)) == len(constants.ROLES)
    assert len(set(constants.TURN_TYPES)) == len(constants.TURN_TYPES)
