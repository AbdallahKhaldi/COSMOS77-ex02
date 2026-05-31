"""Logging init reads logging_config.json and configures dictConfig."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from unittest.mock import patch

import pytest

from cosmos77_ex02.shared import logging_setup


@pytest.fixture
def logging_config_path(tmp_path: Path) -> Path:
    cfg = {
        "version": 1,
        "schema_version": "1.00",
        "disable_existing_loggers": False,
        "formatters": {"std": {"format": "%(message)s"}},
        "handlers": {
            "console": {"class": "logging.StreamHandler", "level": "INFO", "formatter": "std"}
        },
        "loggers": {"cosmos77_ex02": {"level": "DEBUG", "handlers": ["console"]}},
        "root": {"level": "WARNING", "handlers": ["console"]},
    }
    path = tmp_path / "logging_config.json"
    path.write_text(json.dumps(cfg))
    return path


def test_init_logging_calls_dict_config(logging_config_path: Path) -> None:
    with patch("logging.config.dictConfig") as mock_dict_config:
        logging_setup.init_logging(logging_config_path)
    assert mock_dict_config.called
    payload = mock_dict_config.call_args.args[0]
    assert payload["loggers"]["cosmos77_ex02"]["level"] == "DEBUG"


def test_init_logging_uses_default_path() -> None:
    calls: list[dict] = []
    with patch("logging.config.dictConfig", side_effect=lambda p: calls.append(dict(p))):
        logging_setup.init_logging()  # repo config/logging_config.json
    assert calls, "expected default-path logging init to call dictConfig"
    assert calls[0]["handlers"]["fifo_file"]["max_lines_per_file"] == 500


def test_init_logging_creates_fifo_directory(tmp_path: Path) -> None:
    cfg = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {"std": {"format": "%(message)s"}},
        "handlers": {
            "fifo_file": {
                "class": "cosmos77_ex02.shared.fifo_handler.FifoLineRotatingHandler",
                "formatter": "std",
                "directory": str(tmp_path / "logs"),
                "max_files": 2,
                "max_lines_per_file": 3,
            }
        },
        "loggers": {"cosmos77_ex02": {"level": "DEBUG", "handlers": ["fifo_file"]}},
        "root": {"level": "WARNING", "handlers": []},
    }
    path = tmp_path / "logging_config.json"
    path.write_text(json.dumps(cfg))
    with patch("logging.config.dictConfig"):  # exercise _ensure_handler_dirs only
        logging_setup.init_logging(path)
    assert (tmp_path / "logs").exists()


def test_init_logging_creates_file_handler_dir(tmp_path: Path) -> None:
    cfg = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {"std": {"format": "%(message)s"}},
        "handlers": {
            "file": {
                "class": "logging.FileHandler",
                "formatter": "std",
                "filename": str(tmp_path / "nested" / "run.log"),
            }
        },
        "loggers": {"cosmos77_ex02": {"level": "DEBUG", "handlers": ["file"]}},
        "root": {"level": "WARNING", "handlers": []},
    }
    path = tmp_path / "logging_config.json"
    path.write_text(json.dumps(cfg))
    with patch("logging.config.dictConfig"):
        logging_setup.init_logging(path)
    assert (tmp_path / "nested").exists()


def test_get_logger_returns_named_logger() -> None:
    logger = logging_setup.get_logger("cosmos77_ex02.test")
    assert isinstance(logger, logging.Logger)
    assert logger.name == "cosmos77_ex02.test"
