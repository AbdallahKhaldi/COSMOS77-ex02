"""Routing must enforce child -> judge -> child; never child -> child (A5)."""

from __future__ import annotations

import pytest

from cosmos77_ex02.protocol.message import ProtocolMessage
from cosmos77_ex02.protocol.routing import RouteError, is_through_father, validate_route


@pytest.mark.parametrize(
    ("sender", "recipient"),
    [("pro", "judge"), ("con", "judge"), ("judge", "pro"), ("judge", "con")],
)
def test_valid_routes_allowed(sender: str, recipient: str) -> None:
    validate_route(sender, recipient)  # must not raise


@pytest.mark.parametrize(
    ("sender", "recipient"),
    [("pro", "con"), ("con", "pro"), ("judge", "judge"), ("pro", "pro")],
)
def test_invalid_routes_rejected(sender: str, recipient: str) -> None:
    with pytest.raises(RouteError):
        validate_route(sender, recipient)


def test_unknown_sender_rejected() -> None:
    with pytest.raises(RouteError, match="unknown sender"):
        validate_route("moderator", "judge")


def test_is_through_father_true_for_routed_history() -> None:
    history = [("pro", "judge"), ("judge", "con"), ("con", "judge"), ("judge", "pro")]
    assert is_through_father(history) is True


def test_is_through_father_false_when_child_talks_to_child() -> None:
    history = [("pro", "judge"), ("pro", "con")]  # illegal direct hop
    assert is_through_father(history) is False


def test_is_through_father_accepts_message_objects() -> None:
    msgs = [
        ProtocolMessage.create(
            sender="pro", recipient="judge", content="x", ping_no=1, turn_type="opening"
        ),
        ProtocolMessage.create(
            sender="judge", recipient="con", content="y", ping_no=1, turn_type="opening"
        ),
    ]
    assert is_through_father(msgs) is True
