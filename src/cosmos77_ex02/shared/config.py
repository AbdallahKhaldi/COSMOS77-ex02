"""JSON + .env config loader for COSMOS77-ex02 (CLAUDE.md rule 4).

Every module reads its tunables through :class:`Config`, so topic, ping count,
timeouts, the budget cap, and paths are never hardcoded. A future migration to
YAML or a pydantic schema touches only this file.
"""

from __future__ import annotations

import json
import os
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

from cosmos77_ex02.shared.version import validate_config_version

_DEFAULT_CONFIG_DIR = Path(__file__).resolve().parents[3] / "config"
_SENTINEL: Any = object()


class Config:
    """Loads ``setup.json`` (+ ``gatekeeper.json``) and exposes dot-path access."""

    def __init__(self, config_dir: Path | str | None = None) -> None:
        self._config_dir = Path(config_dir) if config_dir is not None else _DEFAULT_CONFIG_DIR
        self._setup = self._load_json("setup.json")
        self._gatekeeper = self._load_json("gatekeeper.json", required=False)
        validate_config_version(str(self._setup.get("version", "")))
        load_dotenv(self._config_dir.parent / ".env", override=False)

    @classmethod
    def from_path(cls, path: Path | str) -> Config:
        """Construct from an explicit ``config/`` directory."""
        return cls(path)

    def _load_json(self, filename: str, *, required: bool = True) -> dict[str, Any]:
        path = self._config_dir / filename
        if not path.exists():
            if required:
                raise FileNotFoundError(f"missing required config file: {path}")
            return {}
        with path.open("r", encoding="utf-8") as fh:
            data = json.load(fh)
        if not isinstance(data, dict):
            raise ValueError(f"{path} must contain a JSON object at the top level")
        return data

    def get(self, dot_path: str, default: Any = _SENTINEL) -> Any:
        """Return the value at ``dot_path`` (e.g. ``debate.pings_per_side``).

        Missing keys raise ``KeyError`` unless ``default`` is supplied.
        """
        node: Any = self._setup
        for part in dot_path.split("."):
            if isinstance(node, Mapping) and part in node:
                node = node[part]
            else:
                if default is _SENTINEL:
                    raise KeyError(dot_path)
                return default
        return node

    def env(self, key: str, default: str | None = None) -> str | None:
        """Read an environment variable (after ``.env`` has been loaded)."""
        return os.environ.get(key, default)

    def debate(self) -> dict[str, Any]:
        """Return the ``debate`` section (topic, positions, pings, word limit)."""
        return dict(self.get("debate", default={}))

    def runtime(self) -> dict[str, Any]:
        """Return the ``runtime`` section (claude CLI path, tools, timeout)."""
        return dict(self.get("runtime", default={}))

    def orchestration(self) -> dict[str, Any]:
        """Return the ``orchestration`` section (watchdog, restarts, transcripts)."""
        return dict(self.get("orchestration", default={}))

    def paths(self) -> dict[str, str]:
        """Return the ``paths`` section (logs_dir, assets_dir)."""
        return dict(self.get("paths", default={}))

    def gatekeeper(self) -> dict[str, Any]:
        """Return the parsed ``gatekeeper.json`` (budget cap, per-call ceiling)."""
        return dict(self._gatekeeper)

    def as_dict(self) -> dict[str, Any]:
        """Return a shallow copy of the underlying ``setup.json`` payload."""
        return dict(self._setup)

    def set(self, dot_path: str, value: Any) -> None:
        """Set the in-memory value at ``dot_path`` (call :meth:`save` to persist)."""
        parts = dot_path.split(".")
        node = self._setup
        for part in parts[:-1]:
            node = node.setdefault(part, {})
        node[parts[-1]] = value

    def save(self) -> None:
        """Write the current setup payload back to ``setup.json``."""
        path = self._config_dir / "setup.json"
        path.write_text(json.dumps(self._setup, indent=2, ensure_ascii=False), encoding="utf-8")

    @property
    def version(self) -> str:
        """The config version string (e.g. ``"1.00"``)."""
        return str(self._setup.get("version", ""))

    @property
    def config_dir(self) -> Path:
        """The directory the loader was pointed at."""
        return self._config_dir

    def __repr__(self) -> str:
        return f"Config(version={self.version!r}, dir={self._config_dir})"
