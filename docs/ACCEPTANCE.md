# Acceptance audit — A1–A15 (UOH-RL07 HW2)

Every acceptance criterion from `../CLAUDE_CODE_PLAYBOOK.md` §1.5 mapped to the
artifact and/or passing test that satisfies it. Verified at the Phase-11 QA cut:
**201 tests pass, 98.11 % coverage, ruff clean, 0 line-cap offenders, CI green.**

| ID | Criterion | Artifact(s) | Test / evidence | Status |
|----|-----------|-------------|-----------------|--------|
| **A1** | Three agents as three OS processes; IPC | `orchestration/process_agent.py` (`AgentProcess`, `multiprocessing` spawn + queues + heartbeat), `orchestration/orchestrator.py` | `tests/unit/test_orchestration/test_process_agent.py` (real spawned-process round-trip + restart); live `transcripts/session_001.json` | ✅ Met |
| **A2** | Distinct Pro/Con Skills; unbiased judge | `skills/skill_pro.md`, `skill_con.md`, `skill_judge.md` | `test_agents/test_skills.py` (distinct Description lines; opposite positions; judge forbids ties/ignores truth) | ✅ Met |
| **A3** | ≥10 pings per side (config-driven) | `config/setup.json` (`pings_per_side: 10`), `orchestration/loop.py` | `test_orchestration/test_orchestrator.py::test_loop_produces_exactly_pings_per_side`; session 1 has 10 Pro + 10 Con turns | ✅ Met |
| **A4** | Mutual rebuttal | `agents/enforcement.py` (`references_opponent`), `JudgeAgent.enforce` | `test_agents/test_enforcement.py`, `test_judge.py::test_enforce_flags_non_rebutting_turn`; session-1 turns rebut | ✅ Met |
| **A5** | Routing child → judge → child | `protocol/routing.py` (`validate_route`, `is_through_father`), orchestrator loop | `test_protocol/test_routing.py`; `test_orchestrator.py::test_every_message_routed_through_judge` (audits session topology) | ✅ Met |
| **A6** | JSON protocol (validated) | `protocol/message.py` (pydantic `ProtocolMessage`), `protocol/serialize.py` | `test_protocol/test_message.py`, `test_serialize.py` (round-trips, validation) | ✅ Met |
| **A7** | Mandatory web search + ≥1 citation/turn | `config/setup.json` (`allowed_tools: [WebSearch]`), `runtime/argv.py` (`--allowedTools`), `protocol/citation.py` (`turn_problems`) | `test_protocol/test_citation.py`; session 1: every debater turn cites a source (31 distinct sources) | ✅ Met |
| **A8** | No tie + justification | `agents/verdict.py` (`Verdict` forbids equal scores), `JudgeAgent.verdict` (`_resolve_winner` breaks ties) | `test_agents/test_verdict.py`, `test_judge.py` (tie-break both ways); session-1 verdict **Con 83 / Pro 79** + justification | ✅ Met |
| **A9** | Real LLM debate (no fabricated text) | `runtime/claude_cli.py` (`claude -p`), `agents/debater.py` | `tests/integration/test_debate_smoke.py` (`live`); session 1 is a real run, $5.86 / 153,926 tokens | ✅ Met |
| **A10** | PC language, turn-taking, word limit | `skills/*.md` (PC rules), `config` (`max_words_per_turn: 180`), `agents/enforcement.py` | `test_protocol/test_citation.py::test_turn_problems_flags_over_length`; session-1 turns ≤180 words | ✅ Met |
| **A11** | Timeouts, watchdog, gatekeeper, SDK, FIFO logs, no hardcode, `.env.example` | `orchestration/watchdog.py`, `shared/gatekeeper.py`, `shared/{logging_setup,fifo_handler}.py`, `sdk/sdk.py`, `config/*.json`, `.env.example` | `test_orchestration/test_watchdog.py`, `test_shared/test_gatekeeper.py`, `test_fifo_handler.py`, `test_sdk/*` | ✅ Met |
| **A12** | Terminal menu | `cli/menu.py`, `cli/main.py`, `cli/actions.py` | `test_cli/test_menu.py`, `test_main.py`; `assets/menu.svg`; `uv run cosmos77-debate --help`/`menu` | ✅ Met |
| **A13** | OOP + committed class diagram | `agents/` hierarchy (`BaseAgent → DebaterAgent → Pro/Con`, `JudgeAgent`) | `docs/diagrams/architecture.mmd` + `assets/architecture.png`; `docs/diagrams/sequence.mmd` + `assets/sequence.png` | ✅ Met |
| **A14** | Reproducible env (uv + pyproject) | `pyproject.toml`, `uv.lock`, `.python-version` | CI runs `uv sync --frozen` on a fresh checkout each push; `uv lock --check` passes | ✅ Met |
| **A15** | README evidence (screenshots, prompts, full session-1 dialogue, cost) | `README.md` (666 lines, 6 images), `transcripts/session_001.json` + `_cost.json`, `assets/`, `docs/prompts/000–011` | README §10 embeds the full dialogue + verdict + interpretation; §12 the cost analysis | ✅ Met |

## HW1 weaknesses closed

| Weakness (HW1) | Fix in HW2 |
|---|---|
| Cost awareness | `shared/gatekeeper.py` token/USD meter + `$5` cap; `orchestration/cost.py` + `SDK.cost_report`; README §12 cost analysis |
| Extensibility | `agents/factory.py` + `BaseAgent` subclassing; `docs/PRD_extension_points.md`; README §13 "How to extend" |
| "Numbers aren't analysis" | `JudgeAgent.verdict` justification grounded in specific turns; README §10 interpretation paragraph |

## Cyber / secrets

`.env` is gitignored and untracked; `.env.example` holds placeholders only; the
pre-commit `detect-private-key` hook runs every commit; no key-shaped strings in
`src/`. The Gatekeeper `scrub()` redacts secrets before logging.

## Quality gates (Phase-11 cut)

- `uv run ruff check .` → 0 · `uv run ruff format --check .` → clean
- `uv run python scripts/check_line_cap.py` → 0 offenders (every `.py` ≤150 lines)
- `uv run pytest -m "not live" --cov-fail-under=85` → **201 passed, 98.11 %**
- `uv lock --check` passes; GitHub Actions green on `main`
- CLAUDE.md unchanged since Phase 0; ≥30 conventional commits, no `wip/tmp`, both authors in `git shortlog`
