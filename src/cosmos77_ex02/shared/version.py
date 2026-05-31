"""Version constant + config-version validation (CLAUDE.md rule 10).

This module is the single source of truth for the project version. Every
``config/*.json`` carries a matching ``"version"`` and is checked against
``VERSION`` at load time so a stale config fails fast instead of silently
driving the system with the wrong knobs.
"""

from __future__ import annotations

from typing import Final

VERSION: Final[str] = "1.00"


def validate_config_version(cfg_version: str) -> None:
    """Raise ``ValueError`` when ``cfg_version`` does not match ``VERSION`` exactly.

    Why exact-match: HW2 pins the major release to 1.00 for the whole
    assignment, so any drift is a mistake, not an upgrade.
    """
    if cfg_version != VERSION:
        raise ValueError(
            f"config version {cfg_version!r} does not match project version {VERSION!r}"
        )
