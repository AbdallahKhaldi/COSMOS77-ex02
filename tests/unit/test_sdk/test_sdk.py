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
        ("build_agent", ("pro",)),
    ],
)
def test_public_methods_raise_not_implemented(method: str, args: tuple) -> None:
    sdk = SDK()
    with pytest.raises(NotImplementedError):
        getattr(sdk, method)(*args)
