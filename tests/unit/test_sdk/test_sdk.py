"""The SDK facade — the single business-logic entry point (rule 2)."""

from __future__ import annotations

import pytest

from cosmos77_ex02.sdk.sdk import SDK
from cosmos77_ex02.shared.config import Config


def test_sdk_builds_with_default_config() -> None:
    sdk = SDK()
    assert isinstance(sdk.config, Config)
    assert sdk.config.get("debate.pings_per_side") == 10


def test_sdk_accepts_injected_config() -> None:
    cfg = Config()
    assert SDK(cfg).config is cfg


def test_run_debate_delegates_to_orchestrator(mocker) -> None:
    fake = mocker.Mock()
    fake.run.return_value = {"transcript_path": "transcripts/session_001.json", "verdict": None}
    orch_cls = mocker.patch(
        "cosmos77_ex02.orchestration.orchestrator.Orchestrator", return_value=fake
    )
    out = SDK().run_debate()
    orch_cls.assert_called_once()
    fake.run.assert_called_once()
    assert out["transcript_path"].endswith("session_001.json")


def test_build_agent_returns_role_specific_agent() -> None:
    from cosmos77_ex02.agents.con import ConAgent
    from cosmos77_ex02.agents.judge import JudgeAgent
    from cosmos77_ex02.agents.pro import ProAgent

    sdk = SDK()
    assert isinstance(sdk.build_agent("pro"), ProAgent)
    assert isinstance(sdk.build_agent("con"), ConAgent)
    assert isinstance(sdk.build_agent("judge"), JudgeAgent)


def test_build_agent_unknown_role_raises() -> None:
    with pytest.raises(ValueError, match="unknown role"):
        SDK().build_agent("moderator")
