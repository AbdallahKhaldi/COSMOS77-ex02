# Prompt log 007 — Phase 7: Judge logic

**Date:** 2026-05-31
**Phase:** 7 — Enforcement, scoring, and the no-tie verdict
**Driver:** Abdallah Khaldi & Tasneem Natour · **Agent:** Claude Code (Opus 4.8)
**Authority:** `../CLAUDE_CODE_PLAYBOOK.md` §9 (Phase 7 prompt)

---

## The prompt issued

> Phase 7 goal: make the judge a real adjudicator (A4, A7, A8, A10) — not a
> passive relay. Strengthen `enforce` (reject/redo on missing citation,
> over-length, failure to rebut, or drift into agreeing — intervene with a role
> reminder); `score_turn` (clarity/evidence/rebuttal/rhetoric — persuasion only,
> truth irrelevant); `verdict` (winner, no tie, differential score, justification
> grounded in turns). Wire `SDK.last_verdict`.

(Full task list: playbook §9.)

## What the agent did (summary)

- **`agents/enforcement.py`** (new) — the judge's quality checks on top of the
  protocol's citation/word-limit rules: `references_opponent` (rebuttal cue or
  keyword overlap; an opening turn needs none), `detect_agreement_drift`
  (catches "I agree", "I concede", …), and `enforcement_problems` combining all
  of them. Kept separate so `judge.py` stays ≤150 lines.
- **`JudgeAgent.enforce`** now takes `opponent_last` and delegates to
  `enforcement_problems` — a non-empty result is the signal to reject the turn /
  intervene (A4, A10).
- **`JudgeAgent.score_turn`** now scores a real persuasion rubric: evidence from
  citation count, **rebuttal high only when the turn engages the opponent**,
  clarity/rhetoric from development — never from truth.
- **`JudgeAgent.verdict`** (from Phase 4) parses the LLM judge's JSON, **breaks any
  tie**, and returns a `Verdict` whose winner has the strictly higher score (A8);
  the `skill_judge` prompt requires the justification to cite specific turns.
- **`SDK.last_verdict`** reads the verdict from the most recent
  `transcripts/session_*.json` (raises if none).

**Tests:** `test_enforcement.py` (drift true/false, rebuttal via cue / overlap /
unrelated, opening turn, combined problems); `test_judge.py` extended
(non-rebutting flagged, agreement drift flagged, score rewards rebuttal);
`test_sdk.py` (`last_verdict` reads the latest transcript; raises when none).

**Verification (playbook §9) — all green:** **172 passed, 1 live deselected,
98.20% coverage**; judge / enforcement / sdk at **100%**; ruff clean; line-cap 0.

## Left for Phase 8

The terminal menu + CLI (`cli/menu.py`, `cli/actions.py`, `cli/render.py`,
`cli/main.py`), all driven through the SDK, with monkeypatched-input tests.
