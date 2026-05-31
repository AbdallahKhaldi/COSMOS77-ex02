"""Keyboard-driven terminal menu over the SDK (acceptance A12).

Holds no business logic: each option dispatches to a handler in
:mod:`cosmos77_ex02.cli.actions`, which calls the SDK. Invalid input re-prompts;
errors (including not-yet-implemented features) are shown without crashing the
loop. ``input_fn`` / ``output_fn`` are injectable for testing.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from cosmos77_ex02.cli import actions
from cosmos77_ex02.cli.render import render_menu
from cosmos77_ex02.sdk.sdk import SDK

_HANDLERS: dict[str, Callable[[Any, Any], str]] = {
    "1": actions.run_debate,
    "2": actions.set_topic,
    "3": actions.set_pings,
    "4": actions.view_verdict,
    "5": actions.tail_logs,
    "6": actions.cost_report,
    "7": actions.diagram_path,
}


class Menu:
    """The interactive menu loop wrapping the SDK."""

    def __init__(
        self,
        sdk: SDK | None = None,
        *,
        input_fn: Callable[[str], str] = input,
        output_fn: Callable[[str], None] = print,
    ) -> None:
        self._sdk = sdk if sdk is not None else SDK()
        self._input = input_fn
        self._output = output_fn

    def run(self) -> None:
        """Render the menu and dispatch choices until the user quits ([0])."""
        while True:
            self._output(render_menu())
            choice = self._input("Select an option: ").strip()
            if choice == "0":
                self._output("Goodbye.")
                return
            handler = _HANDLERS.get(choice)
            if handler is None:
                self._output(f"Invalid choice: {choice!r}. Please pick a listed option.")
                continue
            self._dispatch(handler)

    def _dispatch(self, handler: Callable[[Any, Any], str]) -> None:
        """Run one handler, displaying its result or any error without crashing."""
        try:
            result = handler(self._sdk, self._input)
            if result:
                self._output(result)
        except NotImplementedError:
            self._output("That feature is not available yet.")
        except Exception as exc:  # keep the menu alive on any handler error
            self._output(f"Error: {exc}")
