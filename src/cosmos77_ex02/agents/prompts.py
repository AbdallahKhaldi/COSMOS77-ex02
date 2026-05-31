"""Skill loading, prompt rendering, and citation extraction for agents.

Centralises the text-handling shared by every agent (rule 3): load a Skill
file, build a debater turn prompt from injected context (Context Engineering),
build the judge's verdict prompt, and pull web-source URLs out of a turn.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from cosmos77_ex02.protocol.message import ProtocolMessage
    from cosmos77_ex02.shared.config import Config

SKILLS_DIR = Path(__file__).resolve().parents[1] / "skills"
_URL_RE = re.compile(r"https?://[^\s)>\]\"']+")


def load_skill(filename: str) -> str:
    """Read a Skill markdown file from ``skills/`` (non-empty)."""
    path = SKILLS_DIR / filename
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        raise ValueError(f"skill file is empty: {path}")
    return text


def extract_citations(text: str) -> list[str]:
    """Return the de-duplicated list of web-source URLs found in ``text``."""
    seen: set[str] = set()
    out: list[str] = []
    for raw in _URL_RE.findall(text):
        url = raw.rstrip(".,;")
        if url not in seen:
            seen.add(url)
            out.append(url)
    return out


def count_words(text: str) -> int:
    """Whitespace word count (matches the protocol's ``word_count``)."""
    return len(text.split())


def render_turn_prompt(config: Config, *, position: str, context: dict[str, Any]) -> str:
    """Build a debater's user prompt: rebut, add one point, cite >=1 source."""
    debate = config.debate()
    lines = [
        f"DEBATE TOPIC: {debate.get('topic', '')}",
        f"YOUR POSITION (defend this, never concede): {position}",
        f"This is ping #{context.get('ping_no', 1)}. "
        f"Hard word limit: {debate.get('max_words_per_turn', 180)} words.",
    ]
    if context.get("summary"):
        lines.append(f"Debate so far (running summary): {context['summary']}")
    opponent_last = context.get("opponent_last")
    if opponent_last:
        lines.append(f"Opponent's last argument — rebut it directly:\n{opponent_last}")
    else:
        lines.append("You speak first this round — open with your strongest case.")
    lines.append(
        "Rebut the opponent, advance exactly ONE new point, and cite at least one "
        "real web source. End with a line: 'Sources: <url1>, <url2>'."
    )
    return "\n".join(lines)


def render_verdict_prompt(config: Config, transcript: list[ProtocolMessage]) -> str:
    """Build the judge's verdict prompt from the full transcript."""
    topic = config.debate().get("topic", "")
    body = "\n".join(f"[{m.sender} | ping {m.ping_no}] {m.content}" for m in transcript)
    return (
        f"You are judging a debate on: {topic}\n\nTranscript:\n{body}\n\n"
        "Score PERSUASIVENESS only (never truth). Declare a single winner with a "
        "differential score (the two scores must differ) and a justification that "
        "cites specific turns. Output ONLY the JSON verdict object."
    )
