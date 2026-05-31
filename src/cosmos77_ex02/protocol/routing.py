"""Routing rules — every message goes child -> judge -> child (acceptance A5).

Debaters (``pro`` / ``con``) may only send to and receive from the ``judge``;
the judge may address either debater. A direct child -> child message is
rejected. :func:`is_through_father` audits a whole history for this invariant.
"""

from __future__ import annotations

from typing import Any

_CHILDREN = ("pro", "con")


class RouteError(ValueError):
    """Raised when a message violates the child -> judge -> child routing rule."""


def validate_route(sender: str, recipient: str) -> None:
    """Raise :class:`RouteError` unless ``sender -> recipient`` is permitted."""
    if sender == "judge":
        if recipient not in _CHILDREN:
            raise RouteError(f"judge may only address a debater, not {recipient!r}")
        return
    if sender in _CHILDREN:
        if recipient != "judge":
            raise RouteError(f"{sender!r} may only send to the judge, not {recipient!r}")
        return
    raise RouteError(f"unknown sender {sender!r}")


def _pair(item: Any) -> tuple[str, str]:
    """Extract ``(sender, recipient)`` from a message object or a tuple."""
    if isinstance(item, tuple):
        return item[0], item[1]
    return item.sender, item.recipient


def is_through_father(history: list[Any]) -> bool:
    """Return ``True`` iff no message in ``history`` is a direct child -> child hop."""
    for item in history:
        sender, recipient = _pair(item)
        if sender in _CHILDREN and recipient in _CHILDREN:
            return False
    return True
