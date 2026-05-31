"""Pro/Con debaters: distinct skills/positions; turns rebut + cite (A2, A4, A7)."""

from __future__ import annotations

from cosmos77_ex02.agents.con import ConAgent
from cosmos77_ex02.agents.pro import ProAgent
from tests.unit.test_agents.fakes import FakeRuntime


def test_pro_loads_its_skill_and_position(config, gatekeeper, fake_runtime) -> None:
    pro = ProAgent(fake_runtime, gatekeeper, config)
    assert pro.role == "pro"
    assert "net positive" in pro.position.lower()
    assert "PRO" in pro.skill


def test_con_loads_its_skill_and_position(config, gatekeeper, fake_runtime) -> None:
    con = ConAgent(fake_runtime, gatekeeper, config)
    assert con.role == "con"
    assert "net negative" in con.position.lower()
    assert "CON" in con.skill


def test_pro_and_con_skills_differ(config, gatekeeper) -> None:
    pro = ProAgent(FakeRuntime(), gatekeeper, config)
    con = ConAgent(FakeRuntime(), gatekeeper, config)
    assert pro.skill != con.skill


def test_act_produces_message_with_citation_and_rebuttal_context(
    config, gatekeeper, fake_runtime
) -> None:
    pro = ProAgent(fake_runtime, gatekeeper, config)
    msg = pro.act({"ping_no": 2, "turn_type": "rebuttal", "opponent_last": "OPP-ARGUMENT"})
    assert msg.sender == "pro" and msg.recipient == "judge"
    assert msg.ping_no == 2 and msg.turn_type == "rebuttal"
    assert msg.citations == ["https://example.com/study"]
    assert "OPP-ARGUMENT" in fake_runtime.calls[0]["user"]  # opponent injected for rebuttal
    assert fake_runtime.calls[0]["tools"] == ["WebSearch"]  # mandatory web search


def test_turn_without_sources_yields_no_citations(config, gatekeeper) -> None:
    runtime = FakeRuntime(text="A strong claim with no link at all.")
    msg = ConAgent(runtime, gatekeeper, config).act({"ping_no": 1})
    assert msg.citations == []  # later rejected by JudgeAgent.enforce
