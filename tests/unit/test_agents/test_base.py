"""BaseAgent shared behaviour: metered invocation + message construction."""

from __future__ import annotations

from typing import Any

from cosmos77_ex02.agents.base import BaseAgent
from cosmos77_ex02.protocol.message import ProtocolMessage


class _Dummy(BaseAgent):
    ROLE = "pro"

    def act(self, context: dict[str, Any]) -> ProtocolMessage:
        result = self._invoke("user prompt", allowed_tools=[])
        return self._to_message(
            result.text,
            recipient="judge",
            ping_no=1,
            turn_type="opening",
            citations=["https://x.example"],
            result=result,
        )


def test_invoke_routes_through_gatekeeper(fake_runtime, gatekeeper) -> None:
    agent = _Dummy(fake_runtime, gatekeeper, config=None, skill_text="SKILL-TEXT")
    msg = agent.act({})
    assert isinstance(msg, ProtocolMessage)
    assert gatekeeper.stats.calls == 1  # the call was metered
    assert fake_runtime.calls[0]["system"] == "SKILL-TEXT"  # Skill is the system prompt


def test_to_message_carries_cost_and_tokens(fake_runtime, gatekeeper) -> None:
    agent = _Dummy(fake_runtime, gatekeeper, config=None, skill_text="S")
    msg = agent.act({})
    assert msg.sender == "pro" and msg.recipient == "judge" and msg.role == "pro"
    assert msg.cost_usd == fake_runtime.result.cost_usd
    assert msg.tokens == 30  # 10 input + 20 output
    assert msg.word_count == len(fake_runtime.result.text.split())


def test_role_and_skill_properties(fake_runtime, gatekeeper) -> None:
    agent = _Dummy(fake_runtime, gatekeeper, config=None, skill_text="S")
    assert agent.role == "pro"
    assert agent.skill == "S"
