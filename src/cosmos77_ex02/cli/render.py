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
    """Render a cost report dict as a human-readable block."""
    if not report:
        return "No cost data yet."
    return (
        f"Total: ${report.get('total_cost_usd', 0):.4f} over {report.get('calls', 0)} calls  "
        f"(in {report.get('input_tokens', 0)} / out {report.get('output_tokens', 0)} tokens)  "
        f"remaining ${report.get('remaining_usd', 0):.4f}"
    )


def format_logs(lines: list[str]) -> str:
    """Render a list of log lines (or a placeholder when empty)."""
    return "\n".join(lines) if lines else "No logs yet."
