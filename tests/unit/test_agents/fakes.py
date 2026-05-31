"""Test doubles for the agent layer (no real ``claude`` is ever invoked)."""

from __future__ import annotations

from collections.abc import Sequence

from cosmos77_ex02.runtime.parse import LlmResult

DEFAULT_TURN = "I rebut your point. Here is one new point. Sources: https://example.com/study"
VERDICT_JSON = (
    'Here is my decision:\n{"winner": "pro", "pro_score": 81, "con_score": 74, '
    '"justification": "Pro rebutted in ping 3 and cited a strong source."}'
)


class FakeRuntime:
    """Stand-in for ClaudeCliRuntime that returns a canned LlmResult."""

    def __init__(self, text: str = DEFAULT_TURN, cost: float = 0.01) -> None:
        self.result = LlmResult(text, cost, 10, 20, "sess", False, {"result": text})
        self.calls: list[dict] = []

    def invoke(
        self, system_prompt: str, user_prompt: str, *, allowed_tools: Sequence[str] | None = None
    ) -> LlmResult:
        self.calls.append({"system": system_prompt, "user": user_prompt, "tools": allowed_tools})
        return self.result
