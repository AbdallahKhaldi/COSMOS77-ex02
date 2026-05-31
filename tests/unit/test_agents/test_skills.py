"""The three Skills must exist, be non-empty, and be genuinely distinct (A2)."""

from __future__ import annotations

from pathlib import Path

import pytest

from cosmos77_ex02.agents.prompts import load_skill

SKILLS = ("skill_pro.md", "skill_con.md", "skill_judge.md")


@pytest.mark.parametrize("name", SKILLS)
def test_skill_exists_and_non_empty(name: str) -> None:
    text = load_skill(name)
    assert len(text) > 200


def test_description_lines_are_distinct() -> None:
    firsts = [load_skill(n).splitlines()[0] for n in SKILLS]
    assert all(line.lower().startswith("description:") for line in firsts)
    assert len(set(firsts)) == 3  # genuinely different selectors


def test_pro_and_con_argue_opposite_positions() -> None:
    pro = load_skill("skill_pro.md").lower()
    con = load_skill("skill_con.md").lower()
    assert "net positive" in pro
    assert "net negative" in con


def test_judge_forbids_tie_and_ignores_truth() -> None:
    judge = load_skill("skill_judge.md").lower()
    assert "no tie" in judge or "no tie, ever" in judge
    assert "persuasiveness" in judge or "persuasion" in judge


def test_load_skill_rejects_empty_file(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    empty = tmp_path / "empty.md"
    empty.write_text("   \n")
    monkeypatch.setattr("cosmos77_ex02.agents.prompts.SKILLS_DIR", tmp_path)
    with pytest.raises(ValueError, match="empty"):
        load_skill("empty.md")
