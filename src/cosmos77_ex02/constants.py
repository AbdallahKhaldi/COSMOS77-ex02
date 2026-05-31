"""Core domain constants for the COSMOS77-ex02 debate system.

These are *structural* enumerations, not tunable configuration: the fixed set
of agent roles and turn types that the protocol, agents, and orchestrator all
share. Tunable values (topic, ping count, timeouts, budgets) live in
``config/*.json`` and are read via the Config loader — see CLAUDE.md rule 4.
"""

from __future__ import annotations

ROLES: tuple[str, ...] = ("judge", "pro", "con")
"""The three agent roles. ``judge`` is the father that routes every message;
``pro`` and ``con`` are the debaters that only ever talk through the judge."""

TURN_TYPES: tuple[str, ...] = ("opening", "rebuttal", "closing")
"""The phases a single debate turn can take, in escalating order."""

DEFAULT_ENCODING: str = "utf-8"
"""Encoding for all file and subprocess I/O. Output is English-only (rule: PC,
English) so UTF-8 is a safe, universal default."""
