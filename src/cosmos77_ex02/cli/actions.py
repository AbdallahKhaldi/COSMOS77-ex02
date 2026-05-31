"""Menu action handlers — every action goes through the SDK (rule 2, A12).

Each handler takes the SDK and an ``input_fn`` (so prompts are injectable in
tests) and returns a string to display (or ``None``). No business logic lives
here — handlers only orchestrate SDK calls and rendering.
"""

from __future__ import annotations

from typing import Any

from cosmos77_ex02.cli.render import format_cost, format_logs, format_verdict


def run_debate(sdk: Any, _input: Any) -> str:
    """Run a full debate and report where the transcript landed."""
    result = sdk.run_debate()
    return f"Debate complete. Transcript: {result['transcript_path']}"


def set_topic(sdk: Any, input_fn: Any) -> str:
    """Prompt for a new topic/positions and persist them via the SDK."""
    topic = input_fn("New topic: ").strip()
    pro = input_fn("Pro position (blank to keep): ").strip() or None
    con = input_fn("Con position (blank to keep): ").strip() or None
    sdk.set_topic(topic, pro, con)
    return f"Topic updated to: {topic}"


def set_pings(sdk: Any, input_fn: Any) -> str:
    """Prompt for the pings-per-side count and persist it via the SDK."""
    pings = int(input_fn("Pings per side: ").strip())
    sdk.set_pings(pings)
    return f"Pings per side set to {pings}."


def view_verdict(sdk: Any, _input: Any) -> str:
    """Render the most recent verdict."""
    return format_verdict(sdk.last_verdict())


def tail_logs(sdk: Any, input_fn: Any) -> str:
    """Prompt for a line count and render that many recent log lines."""
    raw = input_fn("How many lines? [50]: ").strip()
    return format_logs(sdk.tail_logs(int(raw) if raw else 50))


def cost_report(sdk: Any, _input: Any) -> str:
    """Render the latest cost report."""
    return format_cost(sdk.cost_report())


def diagram_path(_sdk: Any, _input: Any) -> str:
    """Show where the committed architecture diagrams live."""
    return (
        "Architecture diagrams:\n"
        "  docs/diagrams/architecture.mmd (+ assets/architecture.png)\n"
        "  docs/diagrams/sequence.mmd (+ assets/sequence.png)"
    )
