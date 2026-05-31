"""Citation extraction + per-turn validation (A7)."""

from __future__ import annotations

from cosmos77_ex02.protocol.citation import extract_citations, turn_problems
from cosmos77_ex02.protocol.message import ProtocolMessage
from cosmos77_ex02.shared.config import Config


def _turn(content: str, citations: list[str]) -> ProtocolMessage:
    return ProtocolMessage.create(
        sender="pro",
        recipient="judge",
        content=content,
        ping_no=1,
        turn_type="rebuttal",
        citations=citations,
    )


def test_extract_citations_finds_and_dedupes_urls() -> None:
    text = "per https://x.example/a and https://x.example/a, also https://y.example."
    assert extract_citations(text) == ["https://x.example/a", "https://y.example"]


def test_extract_citations_empty_for_no_urls() -> None:
    assert extract_citations("no links at all") == []


def test_turn_problems_flags_missing_citation() -> None:
    problems = turn_problems(_turn("argument", []), Config())
    assert any("citation" in p for p in problems)


def test_turn_problems_flags_over_length() -> None:
    problems = turn_problems(_turn("word " * 500, ["https://a.example"]), Config())
    assert any("word limit" in p for p in problems)


def test_turn_problems_clean_turn_has_none() -> None:
    assert turn_problems(_turn("short and cited", ["https://a.example"]), Config()) == []


def test_citation_not_required_when_config_disables_it(tmp_path) -> None:
    import json

    cfg_dir = tmp_path / "config"
    cfg_dir.mkdir()
    (cfg_dir / "setup.json").write_text(
        json.dumps(
            {
                "version": "1.00",
                "debate": {"require_citation_per_turn": False, "max_words_per_turn": 180},
            }
        )
    )
    cfg = Config(cfg_dir)
    assert turn_problems(_turn("no citation needed", []), cfg) == []
