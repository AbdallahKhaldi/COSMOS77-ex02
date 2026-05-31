"""Prompt rendering + citation/word helpers."""

from __future__ import annotations

from cosmos77_ex02.agents.prompts import (
    count_words,
    extract_citations,
    render_turn_prompt,
    render_verdict_prompt,
)
from cosmos77_ex02.protocol.message import ProtocolMessage
from cosmos77_ex02.shared.config import Config


def test_extract_citations_dedupes_and_strips_trailing_punctuation() -> None:
    text = "see https://a.example/x, and https://a.example/x. also https://b.example)."
    assert extract_citations(text) == ["https://a.example/x", "https://b.example"]


def test_extract_citations_empty_when_no_urls() -> None:
    assert extract_citations("no links here") == []


def test_count_words() -> None:
    assert count_words("one two three") == 3
    assert count_words("") == 0


def test_render_turn_prompt_includes_topic_position_and_summary() -> None:
    cfg = Config()
    prompt = render_turn_prompt(
        cfg,
        position="NET POSITIVE",
        context={"ping_no": 3, "summary": "S-U-M", "opponent_last": "OPP"},
    )
    assert "NET POSITIVE" in prompt
    assert "ping #3" in prompt
    assert "S-U-M" in prompt and "OPP" in prompt
    assert "Sources:" in prompt


def test_render_turn_prompt_opening_when_no_opponent() -> None:
    prompt = render_turn_prompt(Config(), position="P", context={"ping_no": 1})
    assert "speak first" in prompt


def test_render_verdict_prompt_lists_turns() -> None:
    msgs = [
        ProtocolMessage.create(
            sender="pro", recipient="judge", content="C1", ping_no=1, turn_type="opening"
        ),
        ProtocolMessage.create(
            sender="con", recipient="judge", content="C2", ping_no=1, turn_type="rebuttal"
        ),
    ]
    prompt = render_verdict_prompt(Config(), msgs)
    assert "C1" in prompt and "C2" in prompt
    assert "PERSUASIVENESS" in prompt
