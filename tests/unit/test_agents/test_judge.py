"""JudgeAgent: routing, enforcement, scoring, and the no-tie verdict (A5, A8)."""

from __future__ import annotations

import pytest

from cosmos77_ex02.agents.judge import JudgeAgent
from cosmos77_ex02.agents.verdict import Verdict
from cosmos77_ex02.protocol.message import ProtocolMessage
from tests.unit.test_agents.fakes import FakeRuntime


def _turn(content: str, citations: list[str], *, sender: str = "pro") -> ProtocolMessage:
    return ProtocolMessage.create(
        sender=sender,
        recipient="judge",
        content=content,
        ping_no=1,
        turn_type="rebuttal",
        citations=citations,
    )


def test_relay_forwards_child_message_to_opponent(config, gatekeeper, fake_runtime) -> None:
    judge = JudgeAgent(fake_runtime, gatekeeper, config)
    msg = _turn("Pro says X", ["https://a.example"])
    relayed = judge.relay(msg, "con")
    assert relayed.sender == "judge" and relayed.recipient == "con"
    assert "Pro says X" in relayed.content


def test_act_relays_message_from_context(config, gatekeeper, fake_runtime) -> None:
    judge = JudgeAgent(fake_runtime, gatekeeper, config)
    relayed = judge.act({"message": _turn("hi", ["https://a.example"]), "recipient": "con"})
    assert relayed.recipient == "con" and relayed.sender == "judge"


def test_enforce_flags_missing_citation(config, gatekeeper, fake_runtime) -> None:
    judge = JudgeAgent(fake_runtime, gatekeeper, config)
    problems = judge.enforce(_turn("no source here", []))
    assert any("citation" in p for p in problems)


def test_enforce_flags_over_word_limit(config, gatekeeper, fake_runtime) -> None:
    judge = JudgeAgent(fake_runtime, gatekeeper, config)
    long_turn = _turn("word " * 500, ["https://a.example"])
    problems = judge.enforce(long_turn)
    assert any("word limit" in p for p in problems)


def test_enforce_clean_turn_has_no_problems(config, gatekeeper, fake_runtime) -> None:
    judge = JudgeAgent(fake_runtime, gatekeeper, config)
    assert judge.enforce(_turn("short rebuttal", ["https://a.example"])) == []


def test_score_turn_returns_rubric(config, gatekeeper, fake_runtime) -> None:
    judge = JudgeAgent(fake_runtime, gatekeeper, config)
    scores = judge.score_turn(_turn("a fair length turn here", ["https://a.example"]))
    assert set(scores) == {"clarity", "evidence", "rebuttal", "rhetoric"}


def test_verdict_parses_json_and_names_winner(config, gatekeeper) -> None:
    from tests.unit.test_agents.fakes import VERDICT_JSON

    judge = JudgeAgent(FakeRuntime(text=VERDICT_JSON), gatekeeper, config)
    verdict = judge.verdict([_turn("p", ["https://a.example"])])
    assert isinstance(verdict, Verdict)
    assert verdict.winner == "pro"
    assert verdict.pro_score != verdict.con_score
    assert verdict.justification


def test_verdict_breaks_a_tie(config, gatekeeper) -> None:
    tie = '{"winner": "con", "pro_score": 75, "con_score": 75, "justification": "even"}'
    verdict = JudgeAgent(FakeRuntime(text=tie), gatekeeper, config).verdict([])
    assert verdict.pro_score != verdict.con_score
    assert verdict.winner == "con"  # tie broken in favour of the declared winner


def test_verdict_tie_favours_declared_pro(config, gatekeeper) -> None:
    tie = '{"winner": "pro", "pro_score": 70, "con_score": 70, "justification": "even"}'
    verdict = JudgeAgent(FakeRuntime(text=tie), gatekeeper, config).verdict([])
    assert verdict.winner == "pro"
    assert verdict.pro_score > verdict.con_score


def test_verdict_trusts_higher_score_for_winner(config, gatekeeper) -> None:
    contradiction = '{"winner": "con", "pro_score": 90, "con_score": 60, "justification": "x"}'
    verdict = JudgeAgent(FakeRuntime(text=contradiction), gatekeeper, config).verdict([])
    assert verdict.winner == "pro"  # higher score wins regardless of stated winner


def test_verdict_raises_without_json(config, gatekeeper) -> None:
    judge = JudgeAgent(FakeRuntime(text="no json here"), gatekeeper, config)
    with pytest.raises(ValueError, match="JSON"):
        judge.verdict([])
