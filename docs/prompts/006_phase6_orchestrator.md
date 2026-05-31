# Prompt log 006 — Phase 6: Orchestrator + Watchdog

**Date:** 2026-05-31
**Phase:** 6 — The multi-process orchestrator + watchdog (the working debate)
**Driver:** Abdallah Khaldi & Tasneem Natour · **Agent:** Claude Code (Opus 4.8)
**Authority:** `../CLAUDE_CODE_PLAYBOOK.md` §8 (Phase 6 prompt)

---

## The prompt issued

> Phase 6 goal: the multi-process orchestrator that actually runs the debate,
> plus the watchdog (A1, A3, A4, A5, A9, A11). This is the heart of the grade.
> Strict TDD with mocked agents/runtime; add one integration test behind a
> marker that can run live. Build `process_agent.py` (one agent per process,
> in/out queues, heartbeat), `orchestrator.py` (spawn 3, own transcript, run the
> ping loop, persist session JSON, ask for the verdict), `watchdog.py`
> (timeouts + kill/restart with replay). Wire `SDK.run_debate`.

(Full task list: playbook §8.)

## What the agent did (summary)

Built the working 3-process debate. The orchestrator drives the loop over
*handle* objects, so unit tests inject deterministic in-process fakes while the
real run spawns processes — A1 is proven by a real spawned-process IPC test (no
`claude`), and a `live` smoke test runs the real debate.

- **`orchestration/process_agent.py`** — `AgentProcess`: runs one agent in a
  `multiprocessing` (**spawn**) child with inbound/outbound queues and a shared
  heartbeat; `call(method, timeout=…)` raises `RuntimeTimeout` on stall; the child
  builds its agent itself (runtime/gatekeeper never pickled) and is rebuilt on
  `restart()` (A1).
- **`orchestration/watchdog.py`** — `Watchdog.guarded_call` restarts a dead agent
  before calling and, on a stall (`RuntimeTimeout`), terminates + restarts +
  **replays the same request**, up to `max_restarts_per_agent`; exhaustion raises
  (A11).
- **`orchestration/loop.py`** — the ping loop: Pro → judge relay → Con → judge
  relay, `pings_per_side` rounds; each turn route-validated (child→judge→child,
  A5) and persisted; context carries opponent's last turn + running summary.
- **`orchestration/summary.py` + `transcript.py`** — Context-Engineering summary
  and the incremental `session_NNN.json` writer (A15).
- **`orchestration/orchestrator.py`** — spawns judge/pro/con, runs the loop under
  the watchdog, asks the judge for the no-tie verdict, persists, and returns
  `{transcript_path, verdict, messages}`. Wired into **`SDK.run_debate`** (rule 2).

**Tests (mocked agents; one real-process; one live):** summary; transcript;
watchdog (restart dead, replay stall, exhaustion); orchestrator loop (exactly
`pings_per_side` per side, every message through the judge via `is_through_father`,
no-tie verdict persisted, 4 messages/ping); `AgentProcess` worker + a **real
spawned-process round-trip + restart**; `SDK.run_debate` delegation;
`tests/integration/test_debate_smoke.py` (`live`, 1-ping real debate, excluded
from CI).

**Verification (playbook §8) — all green:** **159 passed, 1 live deselected,
98.11% coverage**; ruff clean; line-cap 0. Live smoke runnable locally with
`uv run pytest -m live`.

## Left for Phase 7

Make the judge a real adjudicator: strengthen `enforce` (rebuttal / agreement-drift
detection) and `score_turn` (LLM persuasion rubric), and harden the verdict.
