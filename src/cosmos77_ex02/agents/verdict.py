"""Verdict — the no-tie adjudication result (acceptance A8).

Validation forbids equal scores and requires that the declared winner is the
side with the higher score, so a tie can never be represented at all.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

_WINNERS = ("pro", "con")


@dataclass
class Verdict:
    """A judged outcome: a winner, differential scores, and a justification."""

    winner: str
    pro_score: int
    con_score: int
    justification: str
    decided_at: str

    def __post_init__(self) -> None:
        if self.winner not in _WINNERS:
            raise ValueError(f"winner must be one of {_WINNERS}, got {self.winner!r}")
        if self.pro_score == self.con_score:
            raise ValueError("verdict must not be a tie: pro_score and con_score must differ")
        if not self.justification.strip():
            raise ValueError("verdict requires a non-empty justification")
        higher = "pro" if self.pro_score > self.con_score else "con"
        if self.winner != higher:
            raise ValueError("winner must be the side with the higher score")

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serialisable view of the verdict."""
        return {
            "winner": self.winner,
            "pro_score": self.pro_score,
            "con_score": self.con_score,
            "justification": self.justification,
            "decided_at": self.decided_at,
        }
