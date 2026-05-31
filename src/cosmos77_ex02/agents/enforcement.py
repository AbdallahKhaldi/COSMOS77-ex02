"""Judge enforcement helpers — rebuttal + anti-collusion checks (A4, A10).

Builds on the protocol's turn rules (citation + word limit) and adds the two
debate-quality checks the judge owns: a turn must actually rebut the opponent,
and a debater must not drift into agreeing with the other side (the judge
intervenes with a role reminder). Kept separate so ``judge.py`` stays small.
"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, Any

from cosmos77_ex02.protocol.citation import turn_problems

if TYPE_CHECKING:
    from cosmos77_ex02.protocol.message import ProtocolMessage

_AGREEMENT = (
    "i agree",
    "you are right",
    "you're right",
    "i concede",
    "i was wrong",
    "i accept your",
    "you have convinced me",
    "i now think you",
)
_REBUTTAL_CUES = (
    "opponent",
    "you claim",
    "you argue",
    "your point",
    "you said",
    "contrary",
    "however",
    "but ",
    "rebut",
    "disagree",
    "counter",
)
_WORD_RE = re.compile(r"[a-z]{5,}")


def detect_agreement_drift(text: str) -> bool:
    """True if the turn drifts into agreeing with / conceding to the opponent."""
    low = text.lower()
    return any(phrase in low for phrase in _AGREEMENT)


def references_opponent(text: str, opponent_last: str | None) -> bool:
    """True if the turn engages the opponent's last point (cue or keyword overlap)."""
    if not opponent_last:
        return True  # an opening turn has nothing to rebut yet
    low = text.lower()
    if any(cue in low for cue in _REBUTTAL_CUES):
        return True
    opponent_words = set(_WORD_RE.findall(opponent_last.lower()))
    turn_words = set(_WORD_RE.findall(low))
    return len(opponent_words & turn_words) >= 2


def enforcement_problems(
    message: ProtocolMessage, config: Any, opponent_last: str | None = None
) -> list[str]:
    """All rule violations: citation/word-limit + rebuttal + anti-collusion."""
    problems = turn_problems(message, config)
    if opponent_last and not references_opponent(message.content, opponent_last):
        problems.append(
            "no rebuttal: the turn must reference and counter the opponent's last point"
        )
    if detect_agreement_drift(message.content):
        problems.append("agreement drift: reminder — defend your assigned position; do not concede")
    return problems
