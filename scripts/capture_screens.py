"""Render clean 'terminal screenshots' of the real program output as SVG.

Uses rich's SVG export to capture the menu, a real debate turn, the verdict, and
the cost report from the committed session transcript — reproducible, with no
manual screen capture (acceptance A15). Run after a real debate:

    uv run python scripts/capture_screens.py

Outputs: assets/menu.svg, assets/debate_turn.svg, assets/verdict.svg,
assets/cost_report.svg.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from cosmos77_ex02.cli.render import render_menu

_WIDTH = 100


def _console() -> Console:
    return Console(record=True, width=_WIDTH)


def capture_menu(out_dir: Path) -> Path:
    """Render the interactive menu."""
    con = _console()
    con.print(render_menu())
    return _save(con, out_dir / "menu.svg", "cosmos77-debate — menu")


def capture_turn(data: dict[str, Any], out_dir: Path) -> Path:
    """Render one real debater turn (the first Pro/Con message)."""
    turn = next((m for m in data.get("messages", []) if m["sender"] in ("pro", "con")), None)
    con = _console()
    if turn is None:
        con.print(Panel("(no debater turn in transcript)", title="Debate turn"))
    else:
        sources = ", ".join(turn.get("citations", [])) or "(none)"
        con.print(
            Panel(
                turn["content"],
                title=f"{turn['sender'].upper()} — ping {turn['ping_no']} ({turn['turn_type']})",
                subtitle=f"Sources: {sources}",
            )
        )
    return _save(con, out_dir / "debate_turn.svg", "cosmos77-debate — live turn")


def capture_verdict(data: dict[str, Any], out_dir: Path) -> Path:
    """Render the no-tie verdict."""
    verdict = data.get("verdict") or {}
    con = _console()
    table = Table(title="Verdict (no tie — judged on persuasiveness)")
    table.add_column("Winner")
    table.add_column("Pro score")
    table.add_column("Con score")
    table.add_row(
        str(verdict.get("winner", "?")).upper(),
        str(verdict.get("pro_score", "?")),
        str(verdict.get("con_score", "?")),
    )
    con.print(table)
    con.print(Panel(verdict.get("justification", "(none)"), title="Justification"))
    return _save(con, out_dir / "verdict.svg", "cosmos77-debate — verdict")


def capture_cost(cost: dict[str, Any], out_dir: Path) -> Path:
    """Render the cost report."""
    con = _console()
    table = Table(title="Cost report")
    table.add_column("Metric")
    table.add_column("Value")
    for key, value in cost.items():
        table.add_row(key, str(value))
    con.print(table)
    return _save(con, out_dir / "cost_report.svg", "cosmos77-debate — cost report")


def _save(con: Console, path: Path, title: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    con.save_svg(str(path), title=title)
    return path


def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def main(argv: list[str] | None = None) -> int:
    """Render all four screenshots from the transcript + cost report."""
    parser = argparse.ArgumentParser(description="Capture terminal screenshots as SVG.")
    parser.add_argument("--transcript", type=Path, default=Path("transcripts/session_001.json"))
    parser.add_argument("--cost", type=Path, default=Path("transcripts/session_001_cost.json"))
    parser.add_argument("--out", type=Path, default=Path("assets"))
    args = parser.parse_args(argv)
    data = _load(args.transcript)
    cost = _load(args.cost)
    produced = [
        capture_menu(args.out),
        capture_turn(data, args.out),
        capture_verdict(data, args.out),
        capture_cost(cost, args.out),
    ]
    for path in produced:
        print(f"wrote {path}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
