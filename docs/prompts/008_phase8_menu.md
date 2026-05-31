# Prompt log 008 — Phase 8: Terminal menu + CLI

**Date:** 2026-05-31
**Phase:** 8 — Keyboard-driven menu + `cosmos77-debate` CLI
**Driver:** Abdallah Khaldi & Tasneem Natour · **Agent:** Claude Code (Opus 4.8)
**Authority:** `../CLAUDE_CODE_PLAYBOOK.md` §10 (Phase 8 prompt)

---

## The prompt issued

> Phase 8 goal: a keyboard-driven terminal menu wrapping the SDK (A12). Use rich
> for rendering, plain input() for selection. Build `cli/menu.py` (8-option menu,
> every option calls an SDK method, invalid input re-prompts), `cli/main.py`
> (argparse with subcommands menu/run/verdict/cost/logs; menu is default). Wire
> `cosmos77-debate`. Monkeypatch input() in tests; SDK mocked.

(Full task list: playbook §10.)

## What the agent did (summary)

Built the operator surface — everything routes through the SDK (rule 2); the CLI
holds no business logic.

- **`SDK` methods wired** — `set_topic` / `set_pings` (persist to `setup.json` via
  the new `Config.set` + `Config.save`) and `tail_logs` (last N JSON-lines across
  the FIFO log files). (`cost_report` remains for Phase 9.)
- **`cli/render.py`** — pure text formatters: the menu screen, verdict, cost
  report, and log tail (no SDK / no `rich`, so output is unit-assertable).
- **`cli/actions.py`** — one handler per option `(sdk, input_fn) -> str`; prompts
  are injected so they are testable.
- **`cli/menu.py`** — `Menu.run()` renders the 8 options, dispatches the choice to
  a handler, **re-prompts on invalid input**, and shows errors (incl. not-yet-
  implemented features) **without crashing the loop**; `[0]` quits.
- **`cli/main.py`** — `cosmos77-debate` argparse entry: `menu` (default) launches
  the loop; `run` / `verdict` / `cost` / `logs -n` are one-shot subcommands;
  `--version` / `--help` work.

**Tests (SDK mocked; input monkeypatched):** menu dispatch (run/set-pings/verdict),
invalid-choice re-prompt, not-implemented + error handled without crashing;
parser subcommands, `--help`/`--version` exit 0, `run`/`logs` delegate to the SDK;
SDK `set_topic`/`set_pings` persistence and `tail_logs`.

**Verification (playbook §10) — green:** **190 passed, 1 live deselected, 98.05%
coverage**; `uv run cosmos77-debate --help` lists the subcommands; `echo "0" | uv
run cosmos77-debate menu` renders the menu and quits. ruff clean; line-cap 0.

## Left for Phase 9

The real debate run (live `claude -p`): produce `transcripts/session_001.json`,
render the architecture + sequence diagrams, capture screenshots, and the cost
report (`SDK.cost_report`). This phase makes live calls — handled with the driver.
