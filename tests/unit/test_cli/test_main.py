"""The argparse entry point: subcommands + delegation to the SDK/menu."""

from __future__ import annotations

import pytest

from cosmos77_ex02.cli.main import build_parser, main


def test_help_exits_zero() -> None:
    with pytest.raises(SystemExit) as exc:
        main(["--help"])
    assert exc.value.code == 0


def test_version_exits_zero() -> None:
    with pytest.raises(SystemExit) as exc:
        main(["--version"])
    assert exc.value.code == 0


@pytest.mark.parametrize("command", ["menu", "run", "verdict", "cost", "logs"])
def test_parser_accepts_each_subcommand(command: str) -> None:
    args = build_parser().parse_args([command])
    assert args.command == command


def test_default_command_launches_menu(mocker) -> None:
    menu = mocker.Mock()
    mocker.patch("cosmos77_ex02.cli.main.Menu", return_value=menu)
    mocker.patch("cosmos77_ex02.cli.main.SDK")
    assert main([]) == 0
    menu.run.assert_called_once()


def test_run_subcommand_invokes_sdk(mocker) -> None:
    sdk = mocker.Mock()
    sdk.run_debate.return_value = {"transcript_path": "t.json"}
    mocker.patch("cosmos77_ex02.cli.main.SDK", return_value=sdk)
    assert main(["run"]) == 0
    sdk.run_debate.assert_called_once()


def test_logs_subcommand_passes_n(mocker) -> None:
    sdk = mocker.Mock()
    sdk.tail_logs.return_value = ["a", "b"]
    mocker.patch("cosmos77_ex02.cli.main.SDK", return_value=sdk)
    assert main(["logs", "-n", "2"]) == 0
    sdk.tail_logs.assert_called_once_with(2)
