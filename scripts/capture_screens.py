"""Render terminal 'screenshots' of the real program output as PNG (A15).

Builds the menu, a real debate turn, the verdict, and the cost report from the
committed transcript with rich (-> SVG), then rasterises to PNG via headless
Chrome (kept as SVG if no browser is found). Reproducible, no manual capture.
Run after a real debate: ``uv run python scripts/capture_screens.py`` ->
assets/{menu,debate_turn,verdict,cost_report}.png.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from cosmos77_ex02.cli.render import render_menu

_WIDTH = 100
_CHROME_CANDIDATES = (
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
)


def _console() -> Console:
    return Console(record=True, width=_WIDTH)


def capture_menu(out_dir: Path) -> Path:
    """Render the interactive menu."""
    con = _console()
    con.print(render_menu())
    return _save(con, out_dir / "menu.png", "cosmos77-debate — menu")


def capture_turn(data: dict[str, Any], out_dir: Path) -> Path:
    """Render one real debater turn (the first Pro/Con message)."""
    turn = next((m for m in data.get("messages", []) if m["sender"] in ("pro", "con")), None)
    con = _console()
    if turn is None:
        con.print(Panel("(no debater turn in transcript)", title="Debate turn"))
    else:
        sub = "Sources: " + (", ".join(turn.get("citations", [])) or "(none)")
        title = f"{turn['sender'].upper()} — ping {turn['ping_no']} ({turn['turn_type']})"
        con.print(Panel(turn["content"], title=title, subtitle=sub))
    return _save(con, out_dir / "debate_turn.png", "cosmos77-debate — live turn")


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
    return _save(con, out_dir / "verdict.png", "cosmos77-debate — verdict")


def capture_cost(cost: dict[str, Any], out_dir: Path) -> Path:
    """Render the cost report."""
    con = _console()
    table = Table(title="Cost report")
    table.add_column("Metric")
    table.add_column("Value")
    for key, value in cost.items():
        table.add_row(key, str(value))
    con.print(table)
    return _save(con, out_dir / "cost_report.png", "cosmos77-debate — cost report")


def _save(con: Console, png_path: Path, title: str) -> Path:
    """Export the console to SVG then rasterise to PNG (SVG kept if no browser)."""
    png_path.parent.mkdir(parents=True, exist_ok=True)
    svg_tmp = png_path.with_suffix(".svg")
    con.save_svg(str(svg_tmp), title=title)
    if _svg_to_png(svg_tmp, png_path):
        svg_tmp.unlink(missing_ok=True)
        return png_path
    return svg_tmp


def _find_chrome() -> str | None:
    for path in _CHROME_CANDIDATES:
        if Path(path).exists():
            return path
    for name in ("google-chrome", "chromium", "chromium-browser", "chrome"):
        found = shutil.which(name)
        if found:
            return found
    return None


def _svg_to_png(svg_path: Path, png_path: Path) -> bool:
    """Rasterise `svg_path` to `png_path` at 2x via headless Chrome (if available)."""
    chrome = _find_chrome()
    box = re.search(r'viewBox="0 0 ([0-9.]+) ([0-9.]+)"', svg_path.read_text(encoding="utf-8"))
    if chrome is None or box is None:
        return False
    width, height = math.ceil(float(box.group(1))), math.ceil(float(box.group(2)))
    cmd = [chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars"]
    cmd += ["--force-device-scale-factor=2", f"--screenshot={png_path}"]
    cmd += [f"--window-size={width},{height}", f"file://{svg_path.resolve()}"]
    subprocess.run(cmd, check=True, capture_output=True)
    return png_path.exists()


def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def main(argv: list[str] | None = None) -> int:
    """Render all four screenshots from the transcript + cost report."""
    parser = argparse.ArgumentParser(description="Capture terminal screenshots as PNG.")
    parser.add_argument("--transcript", type=Path, default=Path("transcripts/session_001.json"))
    parser.add_argument("--cost", type=Path, default=Path("transcripts/session_001_cost.json"))
    parser.add_argument("--out", type=Path, default=Path("assets"))
    args = parser.parse_args(argv)
    data = _load(args.transcript)
    cost = _load(args.cost)
    for path in (
        capture_menu(args.out),
        capture_turn(data, args.out),
        capture_verdict(data, args.out),
        capture_cost(cost, args.out),
    ):
        print(f"wrote {path}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
