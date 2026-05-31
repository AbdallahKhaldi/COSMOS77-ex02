"""The Phase-2 SDK skeleton: a stable facade whose methods are not yet built."""

from __future__ import annotations

import pytest

from cosmos77_ex02.sdk.sdk import SDK
from cosmos77_ex02.shared.config import Config


def test_sdk_builds_with_default_config() -> None:
    sdk = SDK()
    assert isinstance(sdk.config, Config)
    assert sdk.config.get("debate.pings_per_side") == 10


def test_sdk_accepts_injected_config() -> None:
    cfg = Config()
    sdk = SDK(cfg)
    assert sdk.config is cfg


def test_cost_report_not_implemented_until_phase9() -> None:
    with pytest.raises(NotImplementedError):
        SDK().cost_report()


def _sdk_with_tmp_config(tmp_path) -> SDK:
    import json

    from cosmos77_ex02.shared.config import Config

    cfg_dir = tmp_path / "config"
    cfg_dir.mkdir()
    (cfg_dir / "setup.json").write_text(
        json.dumps(
            {
                "version": "1.00",
                "debate": {"topic": "old?", "pings_per_side": 10},
                "paths": {"logs_dir": str(tmp_path / "logs")},
            }
        )
    )
    return SDK(Config(cfg_dir))


def test_set_topic_persists_to_config(tmp_path) -> None:
    import json

    sdk = _sdk_with_tmp_config(tmp_path)
    sdk.set_topic("Is AI good?", pro="AI is good", con="AI is bad")
    saved = json.loads((tmp_path / "config" / "setup.json").read_text())
    assert saved["debate"]["topic"] == "Is AI good?"
    assert saved["debate"]["pro_position"] == "AI is good"


def test_set_pings_persists_to_config(tmp_path) -> None:
    import json

    sdk = _sdk_with_tmp_config(tmp_path)
    sdk.set_pings(3)
    saved = json.loads((tmp_path / "config" / "setup.json").read_text())
    assert saved["debate"]["pings_per_side"] == 3


def test_tail_logs_reads_recent_lines(tmp_path) -> None:
    sdk = _sdk_with_tmp_config(tmp_path)
    logs = tmp_path / "logs"
    logs.mkdir()
    (logs / "debate_00000.jsonl").write_text("\n".join(f"line{i}" for i in range(10)) + "\n")
    assert sdk.tail_logs(3) == ["line7", "line8", "line9"]


def test_tail_logs_empty_when_no_logs(tmp_path) -> None:
    assert _sdk_with_tmp_config(tmp_path).tail_logs() == []


def test_last_verdict_reads_latest_transcript(tmp_path) -> None:
    import json

    from cosmos77_ex02.shared.config import Config

    cfg_dir = tmp_path / "config"
    cfg_dir.mkdir()
    transcripts = tmp_path / "transcripts"
    transcripts.mkdir()
    (cfg_dir / "setup.json").write_text(
        json.dumps({"version": "1.00", "orchestration": {"transcript_dir": str(transcripts)}})
    )
    (transcripts / "session_001.json").write_text(json.dumps({"verdict": {"winner": "con"}}))
    (transcripts / "session_002.json").write_text(
        json.dumps({"verdict": {"winner": "pro", "pro_score": 81, "con_score": 70}})
    )
    verdict = SDK(Config(cfg_dir)).last_verdict()
    assert verdict["winner"] == "pro"  # reads the latest session


def test_last_verdict_raises_when_no_transcript(tmp_path) -> None:
    import json

    from cosmos77_ex02.shared.config import Config

    cfg_dir = tmp_path / "config"
    cfg_dir.mkdir()
    (cfg_dir / "setup.json").write_text(
        json.dumps({"version": "1.00", "orchestration": {"transcript_dir": str(tmp_path / "none")}})
    )
    with pytest.raises(FileNotFoundError, match="no transcript"):
        SDK(Config(cfg_dir)).last_verdict()


def test_run_debate_delegates_to_orchestrator(mocker) -> None:
    fake = mocker.Mock()
    fake.run.return_value = {"transcript_path": "transcripts/session_001.json", "verdict": None}
    orch_cls = mocker.patch(
        "cosmos77_ex02.orchestration.orchestrator.Orchestrator", return_value=fake
    )
    out = SDK().run_debate()
    orch_cls.assert_called_once()
    fake.run.assert_called_once()
    assert out["transcript_path"].endswith("session_001.json")


def test_build_agent_returns_role_specific_agent() -> None:
    from cosmos77_ex02.agents.con import ConAgent
    from cosmos77_ex02.agents.judge import JudgeAgent
    from cosmos77_ex02.agents.pro import ProAgent

    sdk = SDK()
    assert isinstance(sdk.build_agent("pro"), ProAgent)
    assert isinstance(sdk.build_agent("con"), ConAgent)
    assert isinstance(sdk.build_agent("judge"), JudgeAgent)


def test_build_agent_unknown_role_raises() -> None:
    with pytest.raises(ValueError, match="unknown role"):
        SDK().build_agent("moderator")
