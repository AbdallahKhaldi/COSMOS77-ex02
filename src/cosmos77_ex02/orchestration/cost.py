"""Cost aggregation for a finished debate (acceptance A15; closes HW1 cost gap).

Each agent runs in its own process with its own Gatekeeper, so the authoritative
per-call cost lands in the transcript (every ``ProtocolMessage`` carries
``cost_usd`` / ``tokens``). This module sums those into a run cost report:
total USD, tokens, billable calls, cost per ping, and a 10-vs-5-ping projection.
"""

from __future__ import annotations

from typing import Any


def build_cost_report(messages: list[dict[str, Any]], pings_per_side: int) -> dict[str, Any]:
    """Summarise the cost of a debate from its transcript messages."""
    total = round(sum(float(m.get("cost_usd", 0) or 0) for m in messages), 6)
    tokens = sum(int(m.get("tokens", 0) or 0) for m in messages)
    billable = sum(1 for m in messages if float(m.get("cost_usd", 0) or 0) > 0)
    per_ping = round(total / pings_per_side, 6) if pings_per_side else 0.0
    return {
        "total_cost_usd": total,
        "total_tokens": tokens,
        "billable_calls": billable,
        "pings_per_side": pings_per_side,
        "cost_per_ping_usd": per_ping,
        "projected_cost_5_pings_usd": round(per_ping * 5, 6),
        "projected_cost_10_pings_usd": round(per_ping * 10, 6),
    }
