"""The terminal menu dispatches each option to the SDK and stays alive on errors."""

from __future__ import annotations

from unittest.mock import Mock

from cosmos77_ex02.cli.menu import Menu


class InputFeeder:
    """Returns canned responses in order, ignoring the prompt."""

    def __init__(self, responses: list[str]) -> None:
        self._responses = responses
        self._i = 0

    def __call__(self, _prompt: str = "") -> str:
        value = self._responses[self._i]
        self._i += 1
        return value


def _drive(sdk: Mock, inputs: list[str]) -> list[str]:
    out: list[str] = []
    Menu(sdk, input_fn=InputFeeder(inputs), output_fn=out.append).run()
    return out


def test_quit_immediately() -> None:
    out = _drive(Mock(), ["0"])
    assert any("Goodbye" in line for line in out)


def test_run_debate_option_calls_sdk() -> None:
    sdk = Mock()
    sdk.run_debate.return_value = {"transcript_path": "transcripts/session_001.json"}
    out = _drive(sdk, ["1", "0"])
    sdk.run_debate.assert_called_once()
    assert any("session_001.json" in line for line in out)


def test_invalid_choice_reprompts() -> None:
    out = _drive(Mock(), ["9", "0"])
    assert any("Invalid choice" in line for line in out)


def test_set_pings_option_passes_value() -> None:
    sdk = Mock()
    _drive(sdk, ["3", "4", "0"])
    sdk.set_pings.assert_called_once_with(4)


def test_view_verdict_option_renders() -> None:
    sdk = Mock()
    sdk.last_verdict.return_value = {
        "winner": "pro",
        "pro_score": 80,
        "con_score": 70,
        "justification": "clear",
    }
    out = _drive(sdk, ["4", "0"])
    assert any("PRO" in line for line in out)


def test_not_implemented_feature_is_handled() -> None:
    sdk = Mock()
    sdk.cost_report.side_effect = NotImplementedError
    out = _drive(sdk, ["6", "0"])
    assert any("not available" in line for line in out)


def test_handler_error_does_not_crash_menu() -> None:
    sdk = Mock()
    sdk.last_verdict.side_effect = FileNotFoundError("no transcript")
    out = _drive(sdk, ["4", "0"])
    assert any("Error:" in line for line in out)
    assert any("Goodbye" in line for line in out)  # loop survived and quit cleanly
