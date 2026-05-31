# Prompt log 005 — Phase 5: JSON IPC protocol

**Date:** 2026-05-31
**Phase:** 5 — Routing, serialization, and turn validation
**Driver:** Abdallah Khaldi & Tasneem Natour · **Agent:** Claude Code (Opus 4.8)
**Authority:** `../CLAUDE_CODE_PLAYBOOK.md` §7 (Phase 5 prompt)

---

## The prompt issued

> Phase 5 goal: the typed, validated JSON message protocol that carries every
> turn child→judge→child (A5, A6). Strict TDD. `message.py` (pydantic) — done in
> Phase 4. Add `routing.py` (`validate_route`, `is_through_father`),
> `serialize.py` (to_json/from_json), and validation that an over-length or
> citation-less turn fails when `require_citation_per_turn` is true.

(Full task list: playbook §7.)

## What the agent did (summary)

The `ProtocolMessage` model already landed in Phase 4 (agents emit it). Phase 5
adds the rest of the protocol layer and pulls the turn-validation rules into one
place (rule 3).

- **`protocol/routing.py`** — `validate_route(sender, recipient)` enforces that
  debaters only talk to the judge and the judge talks to either debater (any
  child→child or judge→judge hop raises `RouteError`); `is_through_father(history)`
  audits a whole transcript (accepts message objects or `(sender, recipient)`
  tuples) for the child→judge→child invariant (A5).
- **`protocol/citation.py`** — `extract_citations(text)` (URL scrape, de-duped) and
  `turn_problems(message, config)`: the single source of truth for the
  config-driven turn rules (citation required + word limit). `agents/prompts.py`
  now re-exports `extract_citations` from here and **`JudgeAgent.enforce`
  delegates to `turn_problems`** — the rules live in exactly one place.
- **`protocol/serialize.py`** — `to_json`/`from_json` and `to_jsonl`/`from_jsonl`
  (UTF-8) so the orchestrator and FIFO logs persist/reload messages through one
  path; transcripts are JSON-lines (A6).

**Tests (TDD):** `test_routing.py` (valid/invalid routes, unknown sender,
`is_through_father` true/false, message objects); `test_serialize.py` (lossless
JSON + JSON-lines round-trips, invalid payload rejected, blank-line tolerance);
`test_citation.py` (extraction/dedup, missing-citation + over-length flagged,
citation rule disabled via config). Existing agent/judge tests still pass after
the refactor.

**Verification (playbook §7) — all green:** **137 passed, 99.69% coverage**;
protocol modules at **100%**; ruff clean; line-cap 0.

## Left for Phase 6

The multiprocess orchestrator + watchdog (the working debate): `process_agent.py`,
`orchestrator.py`, `loop.py`, `watchdog.py`, `transcript.py`, `summary.py`, with
mocked-agent unit tests and a `live`-marked smoke test.
