"""Tests for the line-based FIFO rotating log handler (20x500 by default)."""

from __future__ import annotations

import json
import logging
from pathlib import Path

from cosmos77_ex02.shared.fifo_handler import FifoLineRotatingHandler


def _logger(handler: logging.Handler, name: str) -> logging.Logger:
    log = logging.getLogger(name)
    log.handlers.clear()
    log.setLevel(logging.DEBUG)
    log.addHandler(handler)
    log.propagate = False
    return log


def test_defaults_are_twenty_files_five_hundred_lines(tmp_path: Path) -> None:
    h = FifoLineRotatingHandler(tmp_path)
    assert h.max_files == 20
    assert h.max_lines_per_file == 500
    assert tmp_path.exists()


def test_rotates_after_max_lines(tmp_path: Path) -> None:
    h = FifoLineRotatingHandler(tmp_path, max_files=5, max_lines_per_file=5)
    h.setFormatter(logging.Formatter("%(message)s"))
    log = _logger(h, "fifo.rotate")
    for i in range(5):
        log.info(json.dumps({"i": i}))
    assert len(sorted(tmp_path.glob("debate_*.jsonl"))) == 1
    log.info(json.dumps({"i": 5}))  # triggers rotation to a 2nd file
    assert len(sorted(tmp_path.glob("debate_*.jsonl"))) == 2


def test_fifo_caps_files_and_lines(tmp_path: Path) -> None:
    max_files, max_lines = 3, 5
    h = FifoLineRotatingHandler(tmp_path, max_files=max_files, max_lines_per_file=max_lines)
    h.setFormatter(logging.Formatter("%(message)s"))
    log = _logger(h, "fifo.cap")
    for i in range(max_files * max_lines * 3):  # far more than the window holds
        log.info(json.dumps({"i": i}))
    files = sorted(tmp_path.glob("debate_*.jsonl"))
    assert len(files) <= max_files
    for f in files:
        assert sum(1 for _ in f.open(encoding="utf-8")) <= max_lines


def test_newest_records_survive_oldest_dropped(tmp_path: Path) -> None:
    h = FifoLineRotatingHandler(tmp_path, max_files=2, max_lines_per_file=2)
    h.setFormatter(logging.Formatter("%(message)s"))
    log = _logger(h, "fifo.newest")
    for i in range(10):
        log.info(str(i))
    kept = "\n".join(p.read_text(encoding="utf-8") for p in sorted(tmp_path.glob("debate_*.jsonl")))
    assert "9" in kept  # newest survived
    assert "0" not in kept.split()  # oldest dropped


def test_resumes_at_existing_index(tmp_path: Path) -> None:
    h1 = FifoLineRotatingHandler(tmp_path, max_files=5, max_lines_per_file=3, prefix="x")
    h1.setFormatter(logging.Formatter("%(message)s"))
    log = _logger(h1, "fifo.resume")
    for i in range(4):  # 3 -> rotate -> 1 in second file (index 1)
        log.info(str(i))
    h2 = FifoLineRotatingHandler(tmp_path, max_files=5, max_lines_per_file=3, prefix="x")
    assert h2._index >= 1
