"""SDK filesystem-backed methods: config persistence, cost report, logs, verdict."""

from __future__ import annotations

import json

import pytest

from cosmos77_ex02.sdk.sdk import SDK
from cosmos77_ex02.shared.config import Config


def _sdk_with_tmp_config(tmp_path) -> SDK:
    cfg_dir = tmp_path / "config"
    cfg_dir.mkdir()
    (cfg_dir / "setup.json").write_text(
        json.dumps(
            {
                "version": "1.00",
                "debate": {"topic": "old?", "pings_per_side": 10},
                "orchestration": {"transcript_dir": str(tmp_path / "transcripts")},
                "paths": {"logs_dir": str(tmp_path / "logs")},
            }
        )
    )
    return SDK(Config(cfg_dir))


def test_set_topic_persists_to_config(tmp_path) -> None:
    sdk = _sdk_with_tmp_config(tmp_path)
    sdk.set_topic("Is AI good?", pro="AI is good", con="AI is bad")
    saved = json.loads((tmp_path / "config" / "setup.json").read_text())
    assert saved["debate"]["topic"] == "Is AI good?"
    assert saved["debate"]["pro_position"] == "AI is good"


def test_set_pings_persists_to_config(tmp_path) -> None:
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


def test_cost_report_summarises_and_persists(tmp_path) -> None:
    sdk = _sdk_with_tmp_config(tmp_path)
    transcripts = tmp_path / "transcripts"
    transcripts.mkdir()
    (transcripts / "session_001.json").write_text(
        json.dumps(
            {
                "pings_per_side": 2,
                "messages": [
                    {"sender": "pro", "cost_usd": 0.10, "tokens": 100},
                    {"sender": "judge", "cost_usd": 0.0, "tokens": 0},
                    {"sender": "con", "cost_usd": 0.30, "tokens": 200},
                ],
            }
        )
    )
    report = sdk.cost_report()
    assert report["total_cost_usd"] == pytest.approx(0.40)
    assert report["billable_calls"] == 2
    assert report["cost_per_ping_usd"] == pytest.approx(0.20)
    assert (transcripts / "session_001_cost.json").exists()


def test_last_verdict_reads_latest_transcript(tmp_path) -> None:
    sdk = _sdk_with_tmp_config(tmp_path)
    transcripts = tmp_path / "transcripts"
    transcripts.mkdir()
    (transcripts / "session_001.json").write_text(json.dumps({"verdict": {"winner": "con"}}))
    (transcripts / "session_002.json").write_text(
        json.dumps({"verdict": {"winner": "pro", "pro_score": 81, "con_score": 70}})
    )
    assert sdk.last_verdict()["winner"] == "pro"  # reads the latest session


def test_last_verdict_raises_when_no_transcript(tmp_path) -> None:
    with pytest.raises(FileNotFoundError, match="no transcript"):
        _sdk_with_tmp_config(tmp_path).last_verdict()
