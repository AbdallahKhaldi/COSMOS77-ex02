# Prompt log 004 — Phase 4: Agent hierarchy + Skills

**Date:** 2026-05-31
**Phase:** 4 — The OOP agent core + the three distinct Skills
**Driver:** Abdallah Khaldi & Tasneem Natour · **Agent:** Claude Code (Opus 4.8)
**Authority:** `../CLAUDE_CODE_PLAYBOOK.md` §6 (Phase 4 prompt)

---

## The prompt issued

> Phase 4 goal: the agent class hierarchy (rule 3: OOP, inheritance, no
> duplication) and the three DISTINCT Skill files. Strict TDD; runtime mocked.
> Build `skills/{skill_pro,skill_con,skill_judge}.md`; `agents/base.py`
> (`BaseAgent`), `debater.py`, `pro.py`/`con.py`, `judge.py`
> (relay/enforce/score_turn/verdict), `factory.py`, `verdict.py`. Wire
> `SDK.build_agent`. ruff zero; coverage ≥90% on agents/.

(Full task list: playbook §6.)

## What the agent did (summary)

Built the OOP core with zero per-side duplication (rule 3) and three genuinely
different Skills (A2). All LLM I/O is mocked.

- **Skills** — `skill_pro.md` (evidence-driven optimist, *net positive*),
  `skill_con.md` (critical skeptic, *net negative*, opposite rhetorical
  strategy), `skill_judge.md` (rules-only, scores persuasion not truth, **no tie
  ever**, emits a JSON verdict). Each opens with a distinct `Description:` line.
- **`protocol/message.py`** (pulled forward from Phase 5, since agents emit it) —
  pydantic `ProtocolMessage` `{msg_id, ts, sender, recipient, role, ping_no,
  turn_type, content, citations[], word_count, tokens, cost_usd}` with role /
  turn-type validators and a `create()` that auto-computes `word_count`.
- **`agents/base.py`** — `BaseAgent(ABC)`: holds role, Skill, runtime, gatekeeper;
  `_invoke()` always routes through `Gatekeeper.guard` (rule 13); `_to_message()`
  builds the `ProtocolMessage` carrying cost/tokens.
- **`agents/prompts.py`** — `load_skill`, `extract_citations` (URL scrape),
  `count_words`, `render_turn_prompt` (Context-Engineering: opponent's last turn +
  running summary), `render_verdict_prompt`.
- **`agents/debater.py` + `pro.py`/`con.py`** — shared turn logic; Pro/Con differ
  only by Skill file + fixed position string.
- **`agents/judge.py`** — `relay` (child→judge→child), `enforce` (citation +
  word-limit), `score_turn` (starter rubric), `verdict` (LLM-driven, parses the
  JSON, **breaks any tie** so a winner always has the strictly higher score).
- **`agents/verdict.py`** — `Verdict` dataclass; validation forbids equal scores
  and an inconsistent winner (A8).
- **`agents/factory.py`** + wired **`SDK.build_agent(role)`** (rule 2 entry point;
  unknown role raises).

**Tests (TDD, runtime+gatekeeper mocked):** skills distinctness; message
validation/round-trip; base metering; Pro/Con loading + citation extraction;
judge relay/enforce/score/verdict (parse, tie-break both ways, no-JSON error);
verdict invariants; factory; SDK.build_agent.

**Verification (playbook §6) — all green:** **114 passed, 99% coverage**; agents
modules 97–100%; ruff clean; line-cap 0; the three skill Description lines are
distinct.

## Left for Phase 5

Harden the protocol layer: `routing.py` (child→judge→child enforcement,
`is_through_father`), `serialize.py`, `citation.py`, and the full protocol
validation test suite.
