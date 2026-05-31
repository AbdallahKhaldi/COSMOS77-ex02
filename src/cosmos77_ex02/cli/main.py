"""CLI entry point for ``cosmos77-debate`` (acceptance A12).

``menu`` (the default) launches the interactive loop; ``run`` / ``verdict`` /
``cost`` / ``logs`` are one-shot subcommands. Everything calls the SDK.
"""

from __future__ import annotations

import argparse
import contextlib
import sys

from cosmos77_ex02.cli import actions
from cosmos77_ex02.cli.menu import Menu
from cosmos77_ex02.cli.render import format_logs
from cosmos77_ex02.sdk.sdk import SDK
from cosmos77_ex02.shared.logging_setup import init_logging
from cosmos77_ex02.shared.version import VERSION


def build_parser() -> argparse.ArgumentParser:
    """Build the argparse parser with the menu/run/verdict/cost/logs subcommands."""
    parser = argparse.ArgumentParser(
        prog="cosmos77-debate", description="AI Agent Debate — Pro vs Con judged by a third agent."
    )
    parser.add_argument("--version", action="version", version=f"cosmos77-ex02 {VERSION}")
    sub = parser.add_subparsers(dest="command")
    sub.add_parser("menu", help="launch the interactive terminal menu (default)")
    sub.add_parser("run", help="run a full debate to a verdict")
    sub.add_parser("verdict", help="show the most recent verdict")
    sub.add_parser("cost", help="show the latest cost report")
    logs = sub.add_parser("logs", help="print the last N structured log lines")
    logs.add_argument("-n", type=int, default=50, help="number of lines (default 50)")
    return parser


def main(argv: list[str] | None = None) -> int:
    """Entry point: dispatch the chosen subcommand (default: the menu)."""
    args = build_parser().parse_args(argv)
    with contextlib.suppress(Exception):  # logging must never block the CLI
        init_logging()
    sdk = SDK()
    command = args.command or "menu"
    if command == "menu":
        Menu(sdk).run()
    elif command == "run":
        print(actions.run_debate(sdk, input))
    elif command == "verdict":
        print(actions.view_verdict(sdk, input))
    elif command == "cost":
        print(actions.cost_report(sdk, input))
    elif command == "logs":
        print(format_logs(sdk.tail_logs(args.n)))
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
