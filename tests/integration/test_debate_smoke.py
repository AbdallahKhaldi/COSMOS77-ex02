"""Live end-to-end smoke test — runs a real 1-ping debate via `claude -p`.

Marked ``live``: EXCLUDED from CI (`-m "not live"`) and run locally only, since
it spawns real processes and bills the Claude Max subscription. It proves the
whole stack works end-to-end with a no-tie verdict and cited turns.
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest

from cosmos77_ex02.orchestration.orchestrator import Orchestrator
from cosmos77_ex02.shared.config import Config


@pytest.mark.live
def test_one_ping_real_debate(tmp_path: Path) -> None:
    repo_config = Path(__file__).resolve().parents[2] / "config"
    cfg_dir = tmp_path / "config"
    cfg_dir.mkdir()
    setup = json.loads((repo_config / "setup.json").read_text(encoding="utf-8"))
    setup["debate"]["pings_per_side"] = 1  # keep the live cost tiny
    setup["orchestration"]["transcript_dir"] = str(tmp_path / "transcripts")
    (cfg_dir / "setup.json").write_text(json.dumps(setup), encoding="utf-8")
    shutil.copy(repo_config / "gatekeeper.json", cfg_dir / "gatekeeper.json")

    result = Orchestrator(Config(cfg_dir)).run()

    assert result["verdict"].winner in ("pro", "con")
    assert result["verdict"].pro_score != result["verdict"].con_score
    data = json.loads(Path(result["transcript_path"]).read_text(encoding="utf-8"))
    debater_turns = [m for m in data["messages"] if m["sender"] in ("pro", "con")]
    assert debater_turns, "expected at least one debater turn"
    assert all(m["citations"] for m in debater_turns), "every debater turn must cite a source"
