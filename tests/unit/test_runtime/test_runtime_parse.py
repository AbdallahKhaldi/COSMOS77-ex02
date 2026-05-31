"""Parsing of the claude -p JSON envelope (happy + error paths)."""

from __future__ import annotations

import pytest

from cosmos77_ex02.runtime.parse import LlmResult, parse_result


def test_parse_valid_result() -> None:
    r = parse_result(
        '{"result":"hi","total_cost_usd":0.5,'
        '"usage":{"input_tokens":3,"output_tokens":4},"session_id":"s","is_error":false}'
    )
    assert isinstance(r, LlmResult)
    assert r.text == "hi"
    assert r.cost_usd == pytest.approx(0.5)
    assert r.input_tokens == 3 and r.output_tokens == 4
    assert r.session_id == "s" and r.is_error is False
    assert r.raw["result"] == "hi"


def test_parse_malformed_json_raises() -> None:
    with pytest.raises(ValueError, match="non-JSON"):
        parse_result("not json {")


def test_parse_non_object_raises() -> None:
    with pytest.raises(ValueError, match="object"):
        parse_result("[1, 2, 3]")


def test_parse_missing_cost_defaults_zero_and_warns(caplog: pytest.LogCaptureFixture) -> None:
    with caplog.at_level("WARNING"):
        r = parse_result('{"result":"x"}')
    assert r.cost_usd == 0.0
    assert any("total_cost_usd" in rec.message for rec in caplog.records)


def test_parse_missing_usage_defaults_zero() -> None:
    r = parse_result('{"result":"x","total_cost_usd":0.1}')
    assert r.input_tokens == 0 and r.output_tokens == 0


def test_parse_null_cost_coerces_to_zero() -> None:
    r = parse_result('{"result":"x","total_cost_usd":null}')
    assert r.cost_usd == 0.0
