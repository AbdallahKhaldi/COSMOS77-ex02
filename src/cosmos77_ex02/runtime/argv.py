"""Build the argv for a headless ``claude -p`` invocation (PRD_agent_base).

Kept as a pure function so the exact CLI surface is unit-testable without ever
spawning a process. The runtime (:mod:`cosmos77_ex02.runtime.claude_cli`) is the
only caller that actually executes the argv.
"""

from __future__ import annotations

from collections.abc import Sequence


def build_argv(
    system_prompt: str,
    user_prompt: str,
    *,
    claude_path: str = "claude",
    output_format: str = "json",
    allowed_tools: Sequence[str] = (),
    max_turns: int | None = None,
) -> list[str]:
    """Return the argument vector for ``claude -p`` with the given options.

    Optional flags are omitted entirely when empty so the command stays minimal
    (and the test surface stays unambiguous).
    """
    argv: list[str] = [claude_path, "-p", user_prompt, "--output-format", output_format]
    if system_prompt:
        argv += ["--append-system-prompt", system_prompt]
    if allowed_tools:
        argv += ["--allowedTools", " ".join(allowed_tools)]
    if max_turns is not None:
        argv += ["--max-turns", str(max_turns)]
    return argv
