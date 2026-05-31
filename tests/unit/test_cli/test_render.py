"""Pure rendering helpers for the terminal menu."""

from __future__ import annotations

from cosmos77_ex02.cli.render import (
    format_cost,
    format_logs,
    format_verdict,
    render_menu,
)


def test_render_menu_lists_all_options() -> None:
    menu = render_menu()
    for key in ("[1]", "[2]", "[3]", "[4]", "[5]", "[6]", "[7]", "[0]"):
        assert key in menu


def test_format_verdict_shows_winner_and_scores() -> None:
    out = format_verdict({"winner": "con", "pro_score": 79, "con_score": 83, "justification": "x"})
    assert "CON" in out and "79" in out and "83" in out


def test_format_verdict_handles_none() -> None:
    assert "run a debate" in format_verdict(None)


def test_format_cost_uses_sdk_report_keys() -> None:
    report = {
        "total_cost_usd": 5.8606,
        "total_tokens": 153926,
        "billable_calls": 20,
        "cost_per_ping_usd": 0.58606,
        "projected_cost_5_pings_usd": 2.9303,
        "projected_cost_10_pings_usd": 5.8606,
    }
    out = format_cost(report)
    assert "5.8606" in out
    assert "20 billable calls" in out
    assert "153926" in out
    assert "2.9303" in out  # 5-ping projection


def test_format_cost_handles_empty() -> None:
    assert "run a debate" in format_cost({})


def test_format_logs() -> None:
    assert format_logs(["a", "b"]) == "a\nb"
    assert "No logs" in format_logs([])
