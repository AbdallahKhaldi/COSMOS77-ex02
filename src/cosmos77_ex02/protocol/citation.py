"""Citation extraction + per-turn validation (acceptance A7, A10).

Owns everything about "is this turn acceptable": pulling web-source URLs out of a
turn and checking the two config-driven turn rules (a citation is required, and
the content must stay within the word limit). The agents and the JudgeAgent both
use these helpers so the rules live in exactly one place (rule 3).
"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from cosmos77_ex02.protocol.message import ProtocolMessage

_URL_RE = re.compile(r"https?://[^\s)>\]\"']+")


def extract_citations(text: str) -> list[str]:
    """Return the de-duplicated web-source URLs found in ``text``."""
    seen: set[str] = set()
    out: list[str] = []
    for raw in _URL_RE.findall(text):
        url = raw.rstrip(".,;")
        if url not in seen:
            seen.add(url)
            out.append(url)
    return out


def turn_problems(message: ProtocolMessage, config: Any) -> list[str]:
    """Return the list of turn-rule violations (empty when the turn is valid).

    Checks the configured ``require_citation_per_turn`` and
    ``max_words_per_turn`` rules — this is the single source of truth the
    JudgeAgent's enforcement delegates to.
    """
    debate = config.debate()
    problems: list[str] = []
    if debate.get("require_citation_per_turn", True) and not message.citations:
        problems.append("missing citation: each debater turn must cite >=1 web source")
    max_words = int(debate.get("max_words_per_turn", 180))
    if message.word_count > max_words:
        problems.append(f"over word limit: {message.word_count} > {max_words}")
    return problems
