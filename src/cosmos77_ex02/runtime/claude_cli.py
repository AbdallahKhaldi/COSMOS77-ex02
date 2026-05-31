"""Headless ``claude -p`` subprocess runtime — the LLM primitive (ADR-001).

This is the only place the project shells out to the ``claude`` CLI. It is
**always mocked in tests** (CLAUDE.md rule 6 / acceptance A9): no unit test ever
spawns the real binary. Agents call it exclusively through the Gatekeeper
(:meth:`cosmos77_ex02.shared.gatekeeper.Gatekeeper.guard`) so every call is
metered against the budget cap.
"""

from __future__ import annotations

import subprocess
from collections.abc import Sequence

from cosmos77_ex02.runtime.argv import build_argv
from cosmos77_ex02.runtime.parse import LlmResult, parse_result
from cosmos77_ex02.shared.config import Config
from cosmos77_ex02.shared.logging_setup import get_logger

_LOG = get_logger("cosmos77_ex02.runtime")


class RuntimeTimeout(RuntimeError):
    """Raised when a ``claude -p`` call exceeds its per-call timeout."""


class ClaudeCliRuntime:
    """Invoke ``claude -p`` headless and return a typed :class:`LlmResult`."""

    def __init__(self, config: Config | None = None) -> None:
        runtime = (config if config is not None else Config()).runtime()
        self._path = str(runtime.get("claude_cli_path", "claude"))
        self._output_format = str(runtime.get("output_format", "json"))
        self._allowed_tools = list(runtime.get("allowed_tools", []))
        self._timeout = int(runtime.get("per_call_timeout_seconds", 120))
        self._max_turns = int(runtime.get("max_turns_per_call", 6))

    def invoke(
        self,
        system_prompt: str,
        user_prompt: str,
        *,
        allowed_tools: Sequence[str] | None = None,
        timeout_s: int | None = None,
    ) -> LlmResult:
        """Run one ``claude -p`` call and return its parsed result.

        Raises :class:`RuntimeTimeout` on timeout and ``RuntimeError`` on a
        non-zero exit or an ``is_error`` result.
        """
        tools = tuple(allowed_tools if allowed_tools is not None else self._allowed_tools)
        argv = build_argv(
            system_prompt,
            user_prompt,
            claude_path=self._path,
            output_format=self._output_format,
            allowed_tools=tools,
            max_turns=self._max_turns,
        )
        timeout = timeout_s if timeout_s is not None else self._timeout
        try:
            proc = subprocess.run(
                argv, capture_output=True, text=True, timeout=timeout, check=False
            )
        except subprocess.TimeoutExpired as exc:
            raise RuntimeTimeout(f"claude -p exceeded {timeout}s") from exc
        if proc.returncode != 0:
            raise RuntimeError(f"claude -p exited {proc.returncode}: {proc.stderr.strip()[:200]}")
        result = parse_result(proc.stdout)
        if result.is_error:
            raise RuntimeError(f"claude -p reported an error: {result.text[:200]}")
        _LOG.debug(
            "claude -p ok: cost=%.4f tokens=%d/%d",
            result.cost_usd,
            result.input_tokens,
            result.output_tokens,
        )
        return result
