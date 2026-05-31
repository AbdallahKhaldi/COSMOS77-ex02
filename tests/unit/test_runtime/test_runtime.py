"""Runtime wrapper: argv construction + invoke behaviour (subprocess mocked).

No test here ever spawns the real ``claude`` binary — ``subprocess.run`` is
patched in every case (CLAUDE.md rule 6 / acceptance A9).
"""

from __future__ import annotations

import subprocess

import pytest

from cosmos77_ex02.runtime.argv import build_argv
from cosmos77_ex02.runtime.claude_cli import ClaudeCliRuntime, RuntimeTimeout

SAMPLE = (
    '{"type":"result","subtype":"success","is_error":false,"result":"hello",'
    '"session_id":"abc","total_cost_usd":0.012,'
    '"usage":{"input_tokens":11,"output_tokens":22}}'
)
_RUN = "cosmos77_ex02.runtime.claude_cli.subprocess.run"


def _completed(stdout: str, code: int = 0, stderr: str = "") -> subprocess.CompletedProcess:
    return subprocess.CompletedProcess(
        args=["claude"], returncode=code, stdout=stdout, stderr=stderr
    )


def test_build_argv_has_core_flags() -> None:
    argv = build_argv(
        "SYS", "USER", claude_path="claude", allowed_tools=("WebSearch",), max_turns=6
    )
    assert argv[:3] == ["claude", "-p", "USER"]
    assert "--output-format" in argv and "json" in argv
    assert "--append-system-prompt" in argv and "SYS" in argv
    assert "--allowedTools" in argv and "WebSearch" in " ".join(argv)
    assert "--max-turns" in argv and "6" in argv


def test_build_argv_omits_optional_when_empty() -> None:
    argv = build_argv("", "U")
    assert "--append-system-prompt" not in argv
    assert "--allowedTools" not in argv
    assert "--max-turns" not in argv


def test_invoke_parses_result(mocker) -> None:
    run = mocker.patch(_RUN, return_value=_completed(SAMPLE))
    res = ClaudeCliRuntime().invoke("sys", "user", allowed_tools=[], timeout_s=60)
    assert res.text == "hello"
    assert res.cost_usd == pytest.approx(0.012)
    assert res.input_tokens == 11 and res.output_tokens == 22
    assert res.session_id == "abc" and res.is_error is False
    run.assert_called_once()


def test_invoke_raises_runtime_timeout(mocker) -> None:
    mocker.patch(_RUN, side_effect=subprocess.TimeoutExpired(cmd="claude", timeout=1))
    with pytest.raises(RuntimeTimeout, match="exceeded"):
        ClaudeCliRuntime().invoke("s", "u", timeout_s=1)


def test_invoke_raises_on_nonzero_exit(mocker) -> None:
    mocker.patch(_RUN, return_value=_completed("", code=2, stderr="boom"))
    with pytest.raises(RuntimeError, match="exited 2"):
        ClaudeCliRuntime().invoke("s", "u")


def test_invoke_raises_on_is_error(mocker) -> None:
    err = '{"is_error":true,"result":"nope","total_cost_usd":0.0}'
    mocker.patch(_RUN, return_value=_completed(err))
    with pytest.raises(RuntimeError, match="error"):
        ClaudeCliRuntime().invoke("s", "u")


def test_invoke_passes_argv_to_subprocess(mocker) -> None:
    run = mocker.patch(_RUN, return_value=_completed(SAMPLE))
    ClaudeCliRuntime().invoke("sys", "user", allowed_tools=["WebSearch"])
    argv = run.call_args.args[0]
    assert argv[0:3] == ["claude", "-p", "user"]
    assert "WebSearch" in " ".join(argv)
