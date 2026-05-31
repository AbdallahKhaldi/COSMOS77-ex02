"""Parse a ``claude -p --output-format json`` result into a typed LlmResult.

The headless JSON envelope carries the response text (``result``), the billed
``total_cost_usd``, token ``usage``, the ``session_id``, and an ``is_error``
flag. Parsing is isolated here so malformed/partial output fails with a clear
message instead of an opaque ``KeyError`` deep in the agent layer.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any

from cosmos77_ex02.shared.logging_setup import get_logger

_LOG = get_logger("cosmos77_ex02.runtime")


@dataclass
class LlmResult:
    """A normalised result from one ``claude -p`` call."""

    text: str
    cost_usd: float
    input_tokens: int
    output_tokens: int
    session_id: str | None
    is_error: bool
    raw: dict[str, Any] = field(default_factory=dict)


def parse_result(stdout: str) -> LlmResult:
    """Parse ``claude -p`` JSON ``stdout`` into an :class:`LlmResult`.

    Raises ``ValueError`` on non-JSON or non-object output. A missing
    ``total_cost_usd`` defaults to ``0.0`` with a warning so the Gatekeeper still
    accounts the call rather than crashing.
    """
    try:
        data = json.loads(stdout)
    except json.JSONDecodeError as exc:
        raise ValueError(f"claude -p returned non-JSON output: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError("claude -p JSON must be an object at the top level")
    if "total_cost_usd" not in data:
        _LOG.warning("claude -p result missing total_cost_usd; defaulting to 0.0")
    usage = data.get("usage") or {}
    return LlmResult(
        text=str(data.get("result", "")),
        cost_usd=float(data.get("total_cost_usd", 0.0) or 0.0),
        input_tokens=int(usage.get("input_tokens", 0) or 0),
        output_tokens=int(usage.get("output_tokens", 0) or 0),
        session_id=data.get("session_id"),
        is_error=bool(data.get("is_error", False)),
        raw=data,
    )
