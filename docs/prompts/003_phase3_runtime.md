# Prompt log 003 — Phase 3: Claude CLI runtime

**Date:** 2026-05-31
**Phase:** 3 — The `claude -p` headless wrapper (the LLM primitive)
**Driver:** Abdallah Khaldi & Tasneem Natour · **Agent:** Claude Code (Opus 4.8)
**Authority:** `../CLAUDE_CODE_PLAYBOOK.md` §5 (Phase 3 prompt)

---

## The prompt issued

> Phase 3 goal: the foundational primitive — a tested wrapper that invokes
> `claude -p` headless and returns structured output. Strict TDD; the real
> subprocess is MOCKED in tests (no live LLM calls ever in the suite). Build
> `runtime/argv.py` (argv), `runtime/parse.py` (JSON → `LlmResult`), and
> `runtime/claude_cli.py` (`ClaudeCliRuntime.invoke`, `RuntimeTimeout`). Wire
> nothing into the debate yet. ruff zero; coverage ≥90% on runtime/.

(Full task list: playbook §5.)

## What the agent did (summary)

Built the single point at which the project shells out to `claude` — and proved
it works without ever spawning the binary (every test patches
`subprocess.run`; acceptance A9).

- **`runtime/argv.py`** — pure `build_argv(...)`: `claude -p <prompt>
  --output-format json [--append-system-prompt …] [--allowedTools …]
  [--max-turns …]`; optional flags omitted when empty.
- **`runtime/parse.py`** — `LlmResult` dataclass `{text, cost_usd, input_tokens,
  output_tokens, session_id, is_error, raw}` + `parse_result(stdout)`: raises a
  clear `ValueError` on non-JSON / non-object output; a missing `total_cost_usd`
  defaults to `0.0` with a warning (so the Gatekeeper still accounts the call).
- **`runtime/claude_cli.py`** — `ClaudeCliRuntime.invoke(...)`: builds argv from
  `Config.runtime()` defaults, runs `subprocess.run(..., timeout=…, check=False)`,
  raises `RuntimeTimeout` on timeout, `RuntimeError` on non-zero exit or an
  `is_error` result, else returns the parsed `LlmResult`. Agents will call it only
  via `Gatekeeper.guard` (Phase 4).

**Tests (TDD, subprocess mocked):** `tests/unit/test_runtime/test_runtime.py`
(argv flags; parse; timeout; non-zero exit; is_error; argv passed to subprocess)
and `test_runtime_parse.py` (valid; malformed JSON; non-object; missing cost +
warning; missing usage; null cost).

**Verification (playbook §5) — all green:** full suite **66 passed, 99.40%
coverage**; runtime modules at **100%**; ruff check + format clean; line-cap 0;
every file ≤150 lines. No test invokes the real `claude` CLI.

## Left for Phase 4

The agent class hierarchy (`BaseAgent → DebaterAgent → Pro/Con`, `JudgeAgent`,
factory, `Verdict`) and the three distinct Skill files — runtime + gatekeeper
mocked.
