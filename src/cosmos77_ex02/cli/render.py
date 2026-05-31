"""Plain-text rendering for the terminal menu (test-friendly).

Kept free of the SDK and of ``rich`` so the menu's output is a pure function of
its inputs and easy to assert in tests. ``main`` may wrap these in ``rich``
panels for nicer display.
"""

from __future__ import annotations

from typing import Any

MENU_OPTIONS: tuple[tuple[str, str], ...] = (
    ("1", "Run debate (current topic)"),
    ("2", "Set topic & positions"),
    ("3", "Set pings per side"),
    ("4", "View last verdict"),
    ("5", "Tail logs (last N)"),
    ("6", "Cost report"),
    ("7", "Show architecture diagram path"),
    ("0", "Quit"),
)


def render_menu() -> str:
    """Return the menu screen as text."""
    body = "\n".join(f"  [{key}] {label}" for key, label in MENU_OPTIONS)
    return f"\n=== COSMOS77-ex02 — AI Agent Debate ===\n{body}\n"


def format_verdict(verdict: Any) -> str:
    """Render a verdict dict (or None) as a human-readable block."""
    if not verdict:
        return "No verdict yet — run a debate first."
    return (
        f"Winner: {verdict.get('winner', '?').upper()}  "
        f"(Pro {verdict.get('pro_score', '?')} / Con {verdict.get('con_score', '?')})\n"
        f"Justification: {verdict.get('justification', '')}"
    )


def format_cost(report: Any) -> str:
    """Render a cost report dict (from SDK.cost_report) as a human-readable block."""
    if not report:
        return "No cost data yet — run a debate first."
    return (
        f"Total: ${report.get('total_cost_usd', 0):.4f} over "
        f"{report.get('billable_calls', 0)} billable calls "
        f"({report.get('total_tokens', 0)} tokens)\n"
        f"Cost/ping: ${report.get('cost_per_ping_usd', 0):.4f}  |  "
        f"projected 5-ping ${report.get('projected_cost_5_pings_usd', 0):.4f} / "
        f"10-ping ${report.get('projected_cost_10_pings_usd', 0):.4f}"
    )


def format_logs(lines: list[str]) -> str:
    """Render a list of log lines (or a placeholder when empty)."""
    return "\n".join(lines) if lines else "No logs yet."
