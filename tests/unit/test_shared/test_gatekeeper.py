"""Tests for the Gatekeeper cost meter + budget cap + secret scrub (rule 13)."""

from __future__ import annotations

from dataclasses import dataclass

import pytest

from cosmos77_ex02.shared.gatekeeper import BudgetExceeded, Gatekeeper

CFG = {"budget_usd_max": 1.0, "per_call_usd_max": 0.5, "warn_at_fraction": 0.8, "hard_stop": True}


def _claude_json(cost: float, in_tok: int = 10, out_tok: int = 20) -> dict:
    """A minimal stand-in for a `claude -p --output-format json` result."""
    return {"total_cost_usd": cost, "usage": {"input_tokens": in_tok, "output_tokens": out_tok}}


def test_account_accrues_cost_and_tokens_from_claude_json() -> None:
    gk = Gatekeeper(CFG)
    gk.account(_claude_json(0.10, 100, 200))
    gk.account(_claude_json(0.05, 5, 7))
    assert gk.stats.total_cost_usd == pytest.approx(0.15)
    assert gk.stats.input_tokens == 105
    assert gk.stats.output_tokens == 207
    assert gk.stats.calls == 2


def test_check_budget_raises_budget_exceeded_at_cap() -> None:
    gk = Gatekeeper(CFG)
    gk.account(_claude_json(1.0))
    with pytest.raises(BudgetExceeded, match="cap"):
        gk.check_budget()


def test_check_budget_silent_under_cap() -> None:
    gk = Gatekeeper(CFG)
    gk.account(_claude_json(0.3))
    gk.check_budget()  # must not raise


def test_hard_stop_false_never_raises() -> None:
    gk = Gatekeeper({**CFG, "hard_stop": False})
    gk.account(_claude_json(5.0))
    gk.check_budget()  # disabled cap -> no raise


def test_warns_at_fraction(caplog: pytest.LogCaptureFixture) -> None:
    gk = Gatekeeper(CFG)
    with caplog.at_level("WARNING"):
        gk.account(_claude_json(0.85))  # 0.85 >= 0.8 * 1.0
    assert any("budget" in r.message.lower() for r in caplog.records)


def test_per_call_ceiling_warns(caplog: pytest.LogCaptureFixture) -> None:
    gk = Gatekeeper(CFG)
    with caplog.at_level("WARNING"):
        gk.account(_claude_json(0.75))  # > per_call_usd_max 0.5
    assert any("per-call" in r.message.lower() for r in caplog.records)


def test_guard_runs_accounts_and_returns() -> None:
    gk = Gatekeeper(CFG)
    result = gk.guard(lambda: _claude_json(0.2, 3, 4))
    assert result["total_cost_usd"] == 0.2
    assert gk.stats.total_cost_usd == pytest.approx(0.2)
    assert gk.stats.calls == 1


def test_guard_pre_check_blocks_when_already_over_budget() -> None:
    gk = Gatekeeper(CFG)
    gk.account(_claude_json(1.0))
    sentinel = {"ran": False}

    def fn() -> dict:
        sentinel["ran"] = True
        return _claude_json(0.0)

    with pytest.raises(BudgetExceeded):
        gk.guard(fn)
    assert sentinel["ran"] is False  # never ran the call


def test_guard_accounts_llmresult_like_object() -> None:
    @dataclass
    class FakeLlmResult:
        cost_usd: float
        input_tokens: int
        output_tokens: int

    gk = Gatekeeper(CFG)
    gk.guard(lambda: FakeLlmResult(0.25, 11, 22))
    assert gk.stats.total_cost_usd == pytest.approx(0.25)
    assert gk.stats.input_tokens == 11
    assert gk.stats.output_tokens == 22


def test_cost_report_fields() -> None:
    gk = Gatekeeper(CFG)
    gk.account(_claude_json(0.4, 1, 2))
    rep = gk.cost_report()
    assert rep["total_cost_usd"] == pytest.approx(0.4)
    assert rep["remaining_usd"] == pytest.approx(0.6)
    assert rep["budget_usd_max"] == 1.0
    assert rep["calls"] == 1


def test_scrub_redacts_keys_but_keeps_surrounding_text() -> None:
    text = "use key sk-ABCD1234efgh5678 and token ghp_ABCDEFGHIJKLMNOPQRST1234 now"
    out = Gatekeeper.scrub(text)
    assert "sk-ABCD1234efgh5678" not in out
    assert "ghp_ABCDEFGHIJKLMNOPQRST1234" not in out
    assert "[REDACTED]" in out
    assert out.startswith("use key ") and out.endswith(" now")


def test_default_config_loads_from_repo() -> None:
    gk = Gatekeeper()  # reads config/gatekeeper.json
    assert gk.budget_usd_max == 5.0
    assert gk.per_call_usd_max == 0.5
