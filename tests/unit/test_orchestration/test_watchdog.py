"""Watchdog: restart a dead agent, replay a stalled call, exhaust restarts."""

from __future__ import annotations

import pytest

from cosmos77_ex02.orchestration.watchdog import Watchdog
from cosmos77_ex02.runtime.claude_cli import RuntimeTimeout
from tests.unit.test_orchestration.helpers import FakeHandle, FlakyResponder


def test_restarts_a_dead_process_before_calling() -> None:
    handle = FakeHandle("pro", lambda m, k: "result")  # starts not-alive
    out = Watchdog(max_restarts=3).guarded_call(handle, "act", 1.0, context={})
    assert out == "result"
    assert handle.restarts == 1 and handle.alive


def test_replays_after_a_stall_then_succeeds() -> None:
    handle = FakeHandle("pro", FlakyResponder(fail_times=2))
    handle.start()
    out = Watchdog(max_restarts=3).guarded_call(handle, "act", 1.0)
    assert out == "ok"
    assert handle.restarts == 2  # restarted once per stall


def test_raises_when_restarts_exhausted() -> None:
    handle = FakeHandle("con", FlakyResponder(fail_times=99))
    handle.start()
    with pytest.raises(RuntimeTimeout):
        Watchdog(max_restarts=2).guarded_call(handle, "act", 1.0)
    assert handle.restarts == 2


def test_dead_with_no_restart_budget_raises() -> None:
    handle = FakeHandle("judge", lambda m, k: "x")  # not alive
    with pytest.raises(RuntimeError, match="exhausted"):
        Watchdog(max_restarts=0).guarded_call(handle, "verdict", 1.0)


def test_is_stalled_detects_dead_or_old_heartbeat() -> None:
    handle = FakeHandle("pro", lambda m, k: "x")
    wd = Watchdog(keepalive_seconds=15)
    assert wd.is_stalled(handle) is True  # not alive
    handle.start()
    assert wd.is_stalled(handle) is False  # heartbeat_age 0
