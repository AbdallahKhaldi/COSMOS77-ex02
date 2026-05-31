# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to a simplified [Semantic Versioning](https://semver.org/)
contract: the major release is pinned to `1.00` for the duration of HW2, with
subsequent minor bumps reserved for post-grading patches.

## [Unreleased]

### Added
- _Phase 12 (submission): cover PDF + `v1.00` tag + release._

## [1.00] — 2026-05-31

### Added

- **Phase 0 (bootstrap)** — repository scaffold and directory layout; package
  skeleton `src/cosmos77_ex02/` (sdk, agents, runtime, orchestration, protocol,
  skills, tools, shared, cli); tooling (`pyproject.toml`, `uv.lock`, ruff,
  pytest with `fail_under = 85`); governance (`CLAUDE.md`, `LICENSE`,
  `CHANGELOG.md`, `CONTRIBUTING.md`, `BADGES.md`); configs (`config/setup.json`,
  `config/gatekeeper.json`, `config/logging_config.json`); quality gates
  (`scripts/check_line_cap.py`, `scripts/generate_cover_pdf.py`,
  `.pre-commit-config.yaml`, `.github/workflows/ci.yml`); core domain constants
  with tests.
- **Phase 1 (docs)** — `docs/PRD.md`, 12 per-mechanism PRDs, `docs/PLAN.md`
  (C4 + sequence diagram + ADRs + risk register), and `docs/TODO.md` with 608
  granular tasks.
- **Phase 2 (shared infra)** — `shared/{version,config,logging_setup,fifo_handler,
  gatekeeper}.py` (Config dot-path loader, FIFO log handler 20×500, Gatekeeper
  token/USD cost meter with budget cap) and the `SDK` skeleton.
- **Phase 3 (runtime)** — `runtime/{argv,parse,claude_cli}.py`: the headless
  `claude -p` JSON wrapper (`LlmResult`, `RuntimeTimeout`), subprocess fully
  mocked in tests.
- **Phase 4 (agents + skills)** — `BaseAgent → DebaterAgent → Pro/Con`,
  `JudgeAgent`, `factory`, `Verdict`; three distinct Pro/Con/Judge Skills;
  `protocol/message.py` (pydantic `ProtocolMessage`).
- **Phase 5 (protocol)** — `protocol/{routing,citation,serialize}.py`:
  child→judge→child routing, citation/word-limit validation, JSON(-lines) I/O.
- **Phase 6 (orchestration)** — `AgentProcess` (one agent per OS process),
  `Watchdog` (timeout + kill/restart + replay), the ping loop, transcript writer,
  running summary, and the `Orchestrator`; wired into `SDK.run_debate`.
- **Phase 7 (judge)** — strengthened enforcement (rebuttal + anti-collusion) and
  a persuasion-scoring rubric; `SDK.last_verdict`.
- **Phase 8 (CLI)** — terminal menu + `cosmos77-debate` argparse entry; SDK
  `set_topic`/`set_pings`/`tail_logs` + `Config.set`/`save`.
- **Phase 9 (real run)** — live 3-process 10-ping debate → `transcripts/session_001.json`
  (no-tie verdict Con 83 / Pro 79, citations on every turn); cost report; rendered
  class + sequence diagrams; four reproducible terminal screenshots; FIFO logging.
- **Phase 10 (README)** — full lab-report README (666 lines, 6 images, full
  session-1 dialogue, cost analysis, self-assessment).
- **Phase 11 (QA)** — `docs/ACCEPTANCE.md` (A1–A15 audit); all gates green.

### Verified at the v1.00 cut

- `uv run ruff check .` / `ruff format --check .` → 0 issues.
- `uv run python scripts/check_line_cap.py` → 0 offenders (every `.py` ≤150 lines).
- `uv run pytest -m "not live" --cov-fail-under=85` → **201 passed, 98.11 % coverage**.
- GitHub Actions CI green on `main`; ≥30 conventional commits, both authors.
- Live debate reproduced end-to-end with a no-tie verdict and cited turns.

### Security

- `.env.example` committed with placeholders only; the real `.env` is excluded
  via `.gitignore`. LLM authentication is the `claude` CLI subscription login —
  no API keys, tokens, or session credentials ship with the repo.
