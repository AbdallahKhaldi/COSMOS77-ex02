"""Contract tests for :class:`cosmos77_ex02.shared.config.Config`.

Config is the single point through which every module reads its tunables, so
these tests pin the dot-path API, the section helpers, the missing-file
behaviour, and the version-validation hook.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from cosmos77_ex02.shared.config import Config


@pytest.fixture
def tmp_config_dir(tmp_path: Path) -> Path:
    """Build a minimal ``config/`` directory inside a tmp tree."""
    cfg_dir = tmp_path / "config"
    cfg_dir.mkdir()
    (cfg_dir / "setup.json").write_text(
        json.dumps(
            {
                "version": "1.00",
                "debate": {"topic": "T?", "pings_per_side": 10, "max_words_per_turn": 180},
                "runtime": {"claude_cli_path": "claude", "per_call_timeout_seconds": 120},
                "orchestration": {"watchdog_keepalive_seconds": 15, "max_restarts_per_agent": 3},
                "paths": {"logs_dir": "logs", "assets_dir": "assets"},
            }
        )
    )
    (cfg_dir / "gatekeeper.json").write_text(
        json.dumps({"version": "1.00", "budget_usd_max": 5.0, "per_call_usd_max": 0.5})
    )
    return cfg_dir


def test_construct_returns_config(tmp_config_dir: Path) -> None:
    assert isinstance(Config(tmp_config_dir), Config)


def test_dot_path_returns_value(tmp_config_dir: Path) -> None:
    cfg = Config(tmp_config_dir)
    assert cfg.get("debate.pings_per_side") == 10
    assert cfg.get("runtime.claude_cli_path") == "claude"


def test_dot_path_returns_default_when_missing(tmp_config_dir: Path) -> None:
    assert Config(tmp_config_dir).get("debate.nope", default=42) == 42


def test_dot_path_raises_when_missing_and_no_default(tmp_config_dir: Path) -> None:
    with pytest.raises(KeyError, match="nope"):
        Config(tmp_config_dir).get("debate.nope")


def test_missing_setup_file_raises(tmp_path: Path) -> None:
    empty = tmp_path / "config"
    empty.mkdir()
    with pytest.raises(FileNotFoundError, match="setup.json"):
        Config(empty)


def test_version_mismatch_raises(tmp_path: Path) -> None:
    cfg_dir = tmp_path / "config"
    cfg_dir.mkdir()
    (cfg_dir / "setup.json").write_text(json.dumps({"version": "0.99", "debate": {}}))
    with pytest.raises(ValueError, match="version"):
        Config(cfg_dir)


def test_non_object_setup_raises(tmp_path: Path) -> None:
    cfg_dir = tmp_path / "config"
    cfg_dir.mkdir()
    (cfg_dir / "setup.json").write_text(json.dumps([1, 2, 3]))
    with pytest.raises(ValueError, match="JSON object"):
        Config(cfg_dir)


def test_section_helpers(tmp_config_dir: Path) -> None:
    cfg = Config(tmp_config_dir)
    assert cfg.debate()["pings_per_side"] == 10
    assert cfg.runtime()["per_call_timeout_seconds"] == 120
    assert cfg.orchestration()["max_restarts_per_agent"] == 3
    assert cfg.paths()["logs_dir"] == "logs"
    assert cfg.gatekeeper()["budget_usd_max"] == 5.0


def test_env_returns_default_when_unset(tmp_config_dir: Path) -> None:
    assert Config(tmp_config_dir).env("COSMOS77_FAKE_KEY", default="fallback") == "fallback"


def test_env_returns_set_value(tmp_config_dir: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("COSMOS77_TEST_VAR", "ok")
    assert Config(tmp_config_dir).env("COSMOS77_TEST_VAR") == "ok"


def test_from_path_and_repr_and_props(tmp_config_dir: Path) -> None:
    cfg = Config.from_path(tmp_config_dir)
    assert cfg.version == "1.00"
    assert cfg.config_dir == tmp_config_dir
    assert "1.00" in repr(cfg)
    assert cfg.as_dict()["version"] == "1.00"


def test_real_repo_config_loads() -> None:
    """The actual config/ directory loads and version-validates."""
    cfg = Config()
    assert cfg.get("debate.pings_per_side") == 10
    assert cfg.gatekeeper()["budget_usd_max"] == 5.0
