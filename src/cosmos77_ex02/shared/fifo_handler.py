"""Line-based FIFO rotating log handler (CLAUDE.md rule; PRD_logging).

A ``logging.Handler`` that writes one JSON-line per record into rolling files
under a directory. When the active file reaches ``max_lines_per_file`` it rolls
to the next index; only the newest ``max_files`` files are kept (oldest is
dropped — first-in-first-out), bounding total log size to
``max_files * max_lines_per_file`` lines regardless of run length.
"""

from __future__ import annotations

import logging
from pathlib import Path


class FifoLineRotatingHandler(logging.Handler):
    """Rotate log files by line count, keeping only the newest N files."""

    def __init__(
        self,
        directory: str | Path,
        max_files: int = 20,
        max_lines_per_file: int = 500,
        encoding: str = "utf-8",
        prefix: str = "debate",
    ) -> None:
        super().__init__()
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)
        self.max_files = int(max_files)
        self.max_lines_per_file = int(max_lines_per_file)
        self.encoding = encoding
        self.prefix = prefix
        self._index = self._initial_index()
        self._lines = self._count_lines(self._path_for(self._index))

    def _path_for(self, index: int) -> Path:
        """Return the file path for a given rotation ``index``."""
        return self.directory / f"{self.prefix}_{index:05d}.jsonl"

    def _initial_index(self) -> int:
        """Resume at the highest existing index, or 0 for a fresh directory."""
        existing = sorted(self.directory.glob(f"{self.prefix}_*.jsonl"))
        if not existing:
            return 0
        return max(int(p.stem.rsplit("_", 1)[-1]) for p in existing)

    @staticmethod
    def _count_lines(path: Path) -> int:
        """Count newline-terminated lines already in ``path`` (0 if absent)."""
        if not path.exists():
            return 0
        with path.open("rb") as fh:
            return sum(1 for _ in fh)

    def _rotate(self) -> None:
        """Advance to the next file and drop the oldest beyond the FIFO window."""
        self._index += 1
        self._lines = 0
        stale = self._path_for(self._index - self.max_files)
        stale.unlink(missing_ok=True)

    def emit(self, record: logging.LogRecord) -> None:
        """Write ``record`` as a single line, rotating first if the file is full."""
        try:
            line = self.format(record)
            if self._lines >= self.max_lines_per_file:
                self._rotate()
            with self._path_for(self._index).open("a", encoding=self.encoding) as fh:
                fh.write(line + "\n")
            self._lines += 1
        except Exception:
            # Logging must never raise into the caller; defer to the stdlib hook.
            self.handleError(record)
