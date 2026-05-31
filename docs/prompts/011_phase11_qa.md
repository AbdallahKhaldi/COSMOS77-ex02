# Prompt log 011 — Phase 11: Final QA gauntlet

**Date:** 2026-05-31
**Phase:** 11 — QA gauntlet + acceptance audit
**Driver:** Abdallah Khaldi & Tasneem Natour · **Agent:** Claude Code (Opus 4.8)
**Authority:** `../CLAUDE_CODE_PLAYBOOK.md` §13 (Phase 11 prompt)

---

## The prompt issued

> Phase 11 goal: every gate green, the real debate reproducible, no acceptance
> criterion unmet. ruff zero + format clean; pytest ≥85%; line-cap 0; integration
> tests for the loop/routing/watchdog/no-tie/SDK/menu; acceptance audit →
> `docs/ACCEPTANCE.md`; secrets scan; `uv lock --check`; CLAUDE.md unchanged;
> commit hygiene; CI green; reproducibility from a fresh clone.

(Full task list: playbook §13.)

## What the agent did (summary)

Ran the full gauntlet and produced the acceptance audit. **No criterion unmet.**

**Gates (all green):**
- `uv run ruff check .` → 0 · `uv run ruff format --check .` → clean (92 files)
- `uv run python scripts/check_line_cap.py` → 0 offenders
- `uv run pytest -m "not live" --cov-fail-under=85` → **201 passed, 98.11 %**
- `uv lock --check` → passes

**Integration coverage (mocked-agent component tests + 1 live):** 10-pings/side
loop (`test_orchestrator`), every message through the judge (`is_through_father`),
watchdog kill/restart (`test_watchdog`), no-tie verdict (`test_verdict`/
`test_judge`), SDK end-to-end (`test_run_debate_delegates` + live smoke), menu via
monkeypatched input (`test_menu`).

**Acceptance audit:** `docs/ACCEPTANCE.md` maps **A1–A15** each to its artifact +
passing test/evidence — all ✅ Met — plus the three HW1-weakness fixes (cost,
extensibility, analysis) and the cyber/secrets posture.

**Security/cyber:** no `.env` tracked; `.env.example` placeholders only; no
key-shaped strings in `src/`; `detect-private-key` pre-commit hook active.

**Hygiene & reproducibility:** CLAUDE.md unchanged since Phase 0 (single commit
touches it); 62 conventional commits, **0** `wip/tmp/fixup`, both authors balanced
in `git shortlog`; working tree clean. Reproducibility is enforced canonically by
CI — every push is a fresh Ubuntu checkout running `uv sync --frozen` + the full
suite, green on `main`. `CHANGELOG.md` expanded to the full `[1.00]` entry across
Phases 0–11.

## Left for Phase 12

Cover PDF (`COSMOS77-ex02.pdf`, exercise number = 2), `v1.00` git tag + GitHub
release, and the manual web-UI steps (collaborator invites + Moodle upload).
