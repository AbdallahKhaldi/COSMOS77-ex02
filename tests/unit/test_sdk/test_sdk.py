"""The Phase-2 SDK skeleton: a stable facade whose methods are not yet built."""

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
    sdk = SDK(cfg)
    assert sdk.config is cfg


@pytest.mark.parametrize(
    ("method", "args"),
    [
        ("run_debate", ()),
        ("set_topic", ("topic",)),
        ("set_pings", (5,)),
        ("last_verdict", ()),
        ("cost_report", ()),
        ("tail_logs", ()),
    ],
)
def test_public_methods_raise_not_implemented(method: str, args: tuple) -> None:
    sdk = SDK()
    with pytest.raises(NotImplementedError):
        getattr(sdk, method)(*args)


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
