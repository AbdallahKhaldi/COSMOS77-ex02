"""The agent factory builds the right class per role and rejects unknown roles."""

from __future__ import annotations

import pytest

from cosmos77_ex02.agents.con import ConAgent
from cosmos77_ex02.agents.factory import build_agent
from cosmos77_ex02.agents.judge import JudgeAgent
from cosmos77_ex02.agents.pro import ProAgent
from tests.unit.test_agents.fakes import FakeRuntime


@pytest.mark.parametrize(
    ("role", "cls"),
    [("pro", ProAgent), ("con", ConAgent), ("judge", JudgeAgent)],
)
def test_build_agent_returns_correct_class(role, cls, config, gatekeeper) -> None:
    agent = build_agent(role, FakeRuntime(), gatekeeper, config)
    assert isinstance(agent, cls)
    assert agent.role == role


def test_build_agent_unknown_role_raises(config, gatekeeper) -> None:
    with pytest.raises(ValueError, match="unknown role"):
        build_agent("moderator", FakeRuntime(), gatekeeper, config)


def test_build_agent_accepts_injected_skill(config, gatekeeper) -> None:
    agent = build_agent("pro", FakeRuntime(), gatekeeper, config, skill_text="CUSTOM")
    assert agent.skill == "CUSTOM"
