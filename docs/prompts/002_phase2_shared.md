# Prompt log 002 — Phase 2: Shared infrastructure

**Date:** 2026-05-31
**Phase:** 2 — Shared layer (port from HW1 + repurpose Gatekeeper + FIFO logs)
**Driver:** Abdallah Khaldi & Tasneem Natour · **Agent:** Claude Code (Opus 4.8)
**Authority:** `../CLAUDE_CODE_PLAYBOOK.md` §4 (Phase 2 prompt)

---

## The prompt issued

> Phase 2 goal: stand up the shared layer by PORTING the proven HW1 modules and
> adapting them. All TDD. Port `cosmos77.shared.{version,config,logging_setup}`,
> ADD a `FifoLineRotatingHandler` (20 files × 500 lines, config-driven),
> REPURPOSE the gatekeeper from an HTTP rate-limiter into an LLM **cost meter**
> (`account`, `check_budget`, `guard`, `scrub`, `BudgetExceeded`), confirm
> `constants.py`, and add the `SDK` skeleton (stubbed methods raising
> `NotImplementedError`). ruff zero; pytest passes; coverage ≥85% on written modules.

(Full task list: playbook §4.)

## What the agent did (summary)

Ported and adapted the HW1 shared modules into `src/cosmos77_ex02/shared/`,
renaming the package and repurposing the gatekeeper. All code is ≤150 lines/file,
fully type-hinted and docstringed; every test mocks I/O (no real `claude`).

- **`shared/version.py`** — `VERSION = "1.00"` + `validate_config_version`; the
  package root re-exports it as `__version__` (single source of truth, rule 10).
- **`shared/config.py`** — `Config` loads `setup.json` (+ `gatekeeper.json`),
  validates the version, loads `.env`, and exposes dot-path `get()` plus
  `debate()/runtime()/orchestration()/paths()/gatekeeper()` section helpers
  (rule 4 — nothing hardcoded).
- **`shared/fifo_handler.py`** — net-new `FifoLineRotatingHandler`: writes
  JSON-lines, rotates at `max_lines_per_file` (500), keeps the newest `max_files`
  (20), drops the oldest (FIFO) — bounding logs to 20×500 regardless of run length.
- **`shared/logging_setup.py`** — `init_logging` (dictConfig + ensures file/FIFO
  dirs) and `get_logger` under the `cosmos77_ex02` namespace.
- **`shared/gatekeeper.py`** — repurposed into a **token/USD cost meter**:
  `account()` reads `total_cost_usd`/`usage` from a `claude -p` JSON (or an
  `LlmResult`); `check_budget()` raises `BudgetExceeded` at `budget_usd_max`;
  `guard()` wraps a call (pre-check → run → account → post-check); `scrub()`
  redacts API-key-shaped secrets; `cost_report()` summarises spend. Config from
  `gatekeeper.json` (rule 13).
- **`sdk/sdk.py`** — `SDK` facade wiring `Config`; public methods stubbed with
  `NotImplementedError` until their phases land (rule 2).

**Tests (TDD, all mocked):** `tests/unit/test_shared/` (version, config,
fifo_handler, logging_setup, gatekeeper) + `tests/unit/test_sdk/`.

**Verification (playbook §4) — all green:** `pytest tests/unit/test_shared/` and
the full suite pass — **53 passed, 99.21% coverage** (gate 85%); the gatekeeper
import smoke (`from cosmos77_ex02.shared.gatekeeper import Gatekeeper`) succeeds;
ruff check + format clean; line-cap 0 offenders.

## Left for Phase 3

The `claude -p` runtime wrapper (`runtime/{argv,parse,claude_cli}.py`,
`LlmResult`, `RuntimeTimeout`) — strict TDD with the subprocess fully mocked.
