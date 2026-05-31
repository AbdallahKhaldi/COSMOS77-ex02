"""Shared fixtures for agent tests — no real ``claude`` is ever invoked."""

from __future__ import annotations

import pytest

from cosmos77_ex02.shared.config import Config
from cosmos77_ex02.shared.gatekeeper import Gatekeeper
from tests.unit.test_agents.fakes import FakeRuntime


@pytest.fixture
def config() -> Config:
    return Config()


@pytest.fixture
def gatekeeper() -> Gatekeeper:
    return Gatekeeper(
        {
            "budget_usd_max": 100.0,
            "per_call_usd_max": 10.0,
            "warn_at_fraction": 0.8,
            "hard_stop": True,
        }
    )


@pytest.fixture
def fake_runtime() -> FakeRuntime:
    return FakeRuntime()
