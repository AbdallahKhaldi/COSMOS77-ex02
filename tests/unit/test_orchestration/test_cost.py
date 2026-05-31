"""Cost report aggregation from transcript messages (A15)."""

from __future__ import annotations

import pytest

from cosmos77_ex02.orchestration.cost import build_cost_report


def _messages() -> list[dict]:
    return [
        {"sender": "pro", "cost_usd": 0.10, "tokens": 100},
        {"sender": "judge", "cost_usd": 0.0, "tokens": 0},  # relay, free
        {"sender": "con", "cost_usd": 0.30, "tokens": 250},
        {"sender": "judge", "cost_usd": 0.05, "tokens": 40},  # verdict
    ]


def test_totals_and_billable_calls() -> None:
    report = build_cost_report(_messages(), pings_per_side=2)
    assert report["total_cost_usd"] == pytest.approx(0.45)
    assert report["total_tokens"] == 390
    assert report["billable_calls"] == 3  # the zero-cost relay is not billable


def test_per_ping_and_projection() -> None:
    report = build_cost_report(_messages(), pings_per_side=2)
    assert report["cost_per_ping_usd"] == pytest.approx(0.225)
    assert report["projected_cost_10_pings_usd"] == pytest.approx(2.25)
    assert report["projected_cost_5_pings_usd"] == pytest.approx(1.125)


def test_zero_pings_is_safe() -> None:
    report = build_cost_report([], pings_per_side=0)
    assert report["total_cost_usd"] == 0.0
    assert report["cost_per_ping_usd"] == 0.0
