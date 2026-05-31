# PRD — Skills (Pro / Con / Judge)

> **Status:** Specification (Phase 1). The three Skill files this document defines are **authored in Phase 4** (playbook §6) under `src/cosmos77_ex02/skills/` as `skill_pro.md`, `skill_con.md`, `skill_judge.md`. This PRD is the binding contract those files must satisfy.
>
> **Scope:** This document covers the *content and contract* of the three Skill prompt files only. The Python classes that **load** these skills (`BaseAgent`, `DebaterAgent`, `ProAgent`, `ConAgent`, `JudgeAgent`) are specified in `docs/PRD_agent_base.md`, `docs/PRD_debater_agents.md`, and `docs/PRD_judge_agent.md`. How a skill is injected into a `claude -p` invocation is specified in `docs/PRD_agent_base.md`. How citations are validated and enforced is specified in `docs/PRD_web_search.md` and `docs/PRD_ipc_protocol.md`.

---

## 1. Purpose and rationale

A "Skill" in this project is a **Markdown prompt file** that defines one agent's persona, rhetorical strategy, and behavioural rules. It is the *Context Engineering* artifact that converts an undifferentiated LLM into a specific, on-character debater or adjudicator. There are exactly three:

| Skill file | Agent | Role string | Position string (from `config/setup.json`) | One-line job |
|---|---|---|---|---|
| `skill_pro.md` | `ProAgent` | `pro` | "Social media is a NET POSITIVE for society." | Evidence-driven optimist; argue NET POSITIVE, never concede. |
| `skill_con.md` | `ConAgent` | `con` | "Social media is a NET NEGATIVE for society." | Critical skeptic; argue NET NEGATIVE with a *different* strategy, never concede. |
| `skill_judge.md` | `JudgeAgent` | `judge` | (none — the judge has no position) | Score persuasiveness, intervene on drift, declare a winner, never tie. |

The three skills exist to satisfy **acceptance criterion A2 (distinct Skills)**: Pro and Con must load *genuinely different* Skill files so the debate produces real contradiction instead of collapsing into agreement, and the judge must load its own Skill that does **not** encode the "right answer," keeping it unbiased. A2 is the single most important requirement this document serves; §6 explains why genuine difference is non-negotiable.

These skills are the project's answer to the course's "Prompt Engineering → Context Engineering" shift (see `docs/PRD.md` §Context): the agents are stateless (per ADR-002 in `docs/PLAN.md`); their *identity* lives entirely in these files plus the orchestrator-injected context, not in a persistent LLM session.

Mapped acceptance criteria: **A2** (primary), **A4** (mutual rebuttal — enforced by debater skills), **A7** (mandatory citation — instructed by debater skills), **A8** (no-tie verdict — instructed by judge skill), **A9** (real LLM debate — the skill shapes the *real* LLM output, never a Python template), **A10** (PC, respectful, turn-taking, word limit).

---

## 2. The Description line drives skill selection

**Every skill file MUST begin with a single one-line `Description:` field as its first content line, before the persona body.** This is not decoration; it is the *selector*. Example shape (final wording is authored in Phase 4):

```
Description: Evidence-driven optimist debater arguing social media is a net positive; rebuts, adds one new point, cites a web source each turn.
```

### 2.1 Why the Description line matters

This project uses the Claude Code Skill convention, where the **one-line Description at the top of a skill is the text a selector reads to decide whether to load that skill.** The body of the skill (persona, rhetoric, rules) is only consulted *after* the Description has caused the skill to be picked. Three consequences for our design:

1. **It is the routing key.** When `factory.build_agent(role, cfg)` (see `docs/PRD_debater_agents.md`) wires an agent to a skill, the Description is the human- and machine-readable summary that makes "this is the Pro debater, not the Con debater, not the judge" unambiguous. A vague or duplicated Description makes selection ambiguous and is treated as a defect.
2. **It must be self-contained and distinct.** A selector that reads only Descriptions must be able to tell the three skills apart from those lines alone — without opening the bodies. Therefore the three Description lines must differ in *role* (debater vs judge), in *position* (pro vs con), and in *strategy framing* (optimist/opportunity vs skeptic/precaution). The Phase 4 acceptance check (`diff <(head -1 skill_pro.md) <(head -1 skill_con.md)`) exists specifically to fail if the first lines are identical.
3. **It front-loads intent so the persona body stays focused.** Because the Description already states *what this agent is*, the body can spend its budget on *how it argues* (rhetoric, constraints) rather than re-establishing identity. This keeps each file small and keeps the injected context token-frugal (supports the Gatekeeper budget; see `docs/PRD_gatekeeper.md`).

### 2.2 Description-line requirements (testable)

- **R-D1** — The first content line of each skill file matches `^Description:\s+\S`.
- **R-D2** — The three Description lines are pairwise distinct (no two skills share a first line).
- **R-D3** — Each Description names the agent's role and, for debaters, its position and its distinctive framing word(s) (e.g., "optimist"/"opportunity" for Pro, "skeptic"/"precaution" for Con).
- **R-D4** — The judge Description states it scores *persuasiveness* and is *position-neutral* (does not reveal a "right answer").

These are verified by `tests/unit/test_agents/` (Phase 4): assert all three files exist, are non-empty, begin with a `Description:` line, and have pairwise-distinct first lines.

---

## 3. `skill_pro.md` — the evidence-driven optimist

### 3.1 Persona

The Pro debater is an **evidence-driven optimist**. It argues, without ever conceding, that **social media is a NET POSITIVE for society** (the `pro_position` string from `config/setup.json`). Its disposition is constructive and forward-looking: it sees social media as infrastructure for human flourishing.

### 3.2 Rhetorical strategy (the "opportunity / benefit-maximization" frame)

Pro argues from **opportunity and gains**. Its thematic toolkit (the skill enumerates these so each turn can draw a *new* point from a fresh theme):

- Democratization of voice — marginalized and minority groups gain a platform.
- Access to information, education, and crisis/health communication.
- Connection — maintaining relationships across distance; community formation.
- Economic value — small-business reach, the creator economy, job creation.
- Civic mobilization and coordination of social movements.

Pro's rhetorical force comes from **concrete benefits, scale, and counterfactuals** ("what would be lost without it"). It reframes harms as solvable design/governance problems rather than intrinsic flaws — this is the structural counter to Con's precaution frame.

### 3.3 Per-turn contract (enforced by the Judge + protocol, see §7)

Every Pro turn MUST:
1. **Rebut** the opponent's immediately-preceding argument explicitly (A4). No parallel monologue.
2. **Advance exactly one NEW point** not used in a prior Pro turn.
3. **Cite ≥1 real web source** discovered via the WebSearch tool (A7); the citation is emitted in the protocol message's `citations[]` array (see `docs/PRD_ipc_protocol.md`).
4. **Stay within `max_words_per_turn` = 180 words** (A10).
5. **Stay PC and respectful** — argue the position, never attack the person (A10).
6. **Never concede the overall position** — Pro may grant a minor point rhetorically but must always conclude that social media is a net positive.

### 3.4 Constraints

- English only (CLAUDE.md §English-only).
- Lies are *permitted* (A8) — Pro may rhetorically overstate or cherry-pick; it is the Con debater's job to catch this, not the judge's. The skill must NOT instruct the model to be factually scrupulous at the expense of persuasiveness; persuasion is what is graded.

---

## 4. `skill_con.md` — the critical skeptic

### 4.1 Persona

The Con debater is a **critical skeptic**. It argues, without ever conceding, that **social media is a NET NEGATIVE for society** (the `con_position` string from `config/setup.json`). Its disposition is wary and harm-focused: it treats social media as a system whose costs are systemic and under-priced.

### 4.2 Rhetorical strategy — DELIBERATELY DIFFERENT from Pro (the "risk / precaution" frame)

This is the heart of A2. Con must use a **different argumentative strategy**, not merely the opposite conclusion. Where Pro maximizes *benefits*, Con applies **risk and the precautionary principle**: it emphasizes harms, externalities, asymmetric and irreversible damage, and burden-of-proof shifting onto the optimist.

Con's thematic toolkit (one new theme per turn):

- Mental-health harms — anxiety, depression, especially among adolescents.
- Misinformation and disinformation at scale; erosion of shared facts.
- Addiction and the attention economy — engagement-maximizing design.
- Political and social polarization; filter bubbles and outrage amplification.
- Privacy erosion and surveillance/data-exploitation business models.

Con's rhetorical force comes from **cumulative-harm framing, externalities the optimist ignores, and reframing Pro's "benefits" as the bait of an extractive system**. Critically, Con's *mode of argument* (precaution, downside-weighting, systemic critique) is structurally distinct from Pro's (opportunity, upside-weighting, solvable-problem framing) — that structural distinction, not just the opposite verdict, is what prevents the debate from collapsing into two mirror-image monologues.

### 4.3 Per-turn contract

Identical structural obligations to Pro (§3.3): rebut (A4), one new point, ≥1 citation (A7), ≤180 words (A10), PC (A10), never concede. The *content and framing* differ; the *contract* is symmetric so the judge can score both sides on equal footing.

### 4.4 Constraints

Same as Pro (§3.4): English only; lies permitted and expected to be caught by the opponent (A8).

---

## 5. `skill_judge.md` — the rubric (knows only the rules)

### 5.1 Persona and the deliberate ignorance principle

The Judge is the **father process** (A1, A5). It knows **only the rules of the debate game** — it does **NOT** know, and must never be told, the "right answer" to the topic. This deliberate ignorance is what keeps it unbiased: it cannot favour a side on the merits of the topic because it has no opinion on the merits. It evaluates *how well each side argues*, not *who is correct*. (Routing, turn-taking, ping counting, and verdict mechanics for the Python `JudgeAgent` are in `docs/PRD_judge_agent.md`; this section specifies the *prompt* that shapes the LLM's judging behaviour.)

### 5.2 Scoring rubric — PERSUASIVENESS only, never factual truth

The judge scores each debater turn (and aggregates across the debate) on four persuasiveness dimensions, and **explicitly not** on factual correctness:

| Dimension | What it measures |
|---|---|
| **Clarity** | Is the argument well-structured, easy to follow, unambiguous? |
| **Evidence use** | Is the cited source deployed effectively and relevantly (regardless of whether it is true)? |
| **Rebuttal quality** | Does the turn engage and dismantle the opponent's last point (A4)? |
| **Rhetorical force** | Persuasive power — framing, emphasis, memorable phrasing. |

The skill MUST state plainly: **truth is irrelevant to the score; lies are allowed; a lie that the opponent fails to catch may legitimately score well on persuasiveness.** Catching lies is the *opponent's* job, and a successful catch scores as *rebuttal quality* — the judge rewards the catch, it does not fact-check on the debaters' behalf.

### 5.3 The no-tie mandate (A8)

The judge **MUST declare exactly one winner** with a **differential score** (e.g., `Pro 80 / Con 73`) and a **written justification grounded in specific turns**. The skill forbids ties absolutely:

- Scores must be **unequal**. Equal scores or the word "tie" are invalid output.
- If the aggregate scores would otherwise be close, the skill instructs the judge to **break the near-tie on rebuttal quality** (the dimension that best reflects genuine engagement).
- The justification must reference **specific turns/pings** (e.g., "Con's ping-7 rebuttal on adolescent mental health went unanswered"), not generic praise — this closes the HW1 "numbers aren't analysis" weakness (playbook §0.0).

The structured `Verdict` object (`agents/verdict.py`, Phase 7) enforces this contract in code: validation rejects equal scores or a missing winner (see `docs/PRD_judge_agent.md`).

### 5.4 Intervention on drift (anti-collusion)

If a debater **drifts into agreeing** with the opponent, concedes its position, stops rebutting, or otherwise breaks character, the judge **intervenes**: it issues a role-reminder relay note ("You are arguing the NET POSITIVE position; restate and rebut") and requests a redo, rather than scoring the off-position turn. This protects A2 (genuine contradiction) and A4 (mutual rebuttal) at runtime, even if a debater's LLM output momentarily softens. The enforcement hooks (`JudgeAgent.enforce`) are specified in `docs/PRD_judge_agent.md`; this skill supplies the *criteria* the judge uses to detect drift.

### 5.5 Constraints

- Position-neutral: the skill must contain **no statement of which side is correct**.
- English only.
- Output a parseable verdict (winner + two unequal integer scores + justification) consumable by `agents/verdict.py`.

---

## 6. Why the personas MUST be genuinely different (A2)

This section is the rationale the grader will look for. A2 is graded, and the playbook (§0.0, §0.1) flags "agents auto-agreeing" as a top risk.

**The failure mode A2 prevents.** If Pro and Con loaded the same (or near-identical) skill, the two LLM instances — drawn from the same base model — would converge. The "debate" would degenerate into two agents nodding at each other, producing parallel monologues or, worse, mutual agreement. That destroys the entire point of the assignment (a *contested* debate judged to a winner) and would make A4 (mutual rebuttal), A8 (a meaningful winner), and the whole 45%-weighted "working debate" hollow.

**Difference must be structural, not cosmetic.** Opposite *conclusions* alone are insufficient. Two agents that both reason "maximize benefits / minimize harms" and merely flip the final verdict produce mirror-image arguments that talk past each other. Genuine contradiction requires **different argumentative strategies**:

- Pro reasons from **opportunity / upside / benefit-maximization** and treats harms as solvable design problems.
- Con reasons from **risk / precaution / downside-weighting** and treats benefits as the bait of an extractive system.

Because the *frames* differ, each side naturally attacks the other's blind spot (Con presses the externalities Pro's optimism ignores; Pro presses the counterfactual losses Con's precaution ignores), which *generates* rebuttal material turn after turn and keeps the 10 pings/side substantive.

**The judge's difference is its neutrality.** The judge is "different" along a third axis: it has *no position at all*. Its ignorance of the right answer (§5.1) is what makes its winner-declaration credible. A judge that knew the answer would be biased; a judge that scored truth would be fact-checking, not adjudicating persuasion.

**How difference is verified.**
- **Description-line distinctness** (R-D2) — the Phase 4 `diff` check fails if Pro and Con share a first line.
- **Content distinctness** — Phase 4 tests assert the three skill bodies are non-empty and differ; the per-turn contracts share *structure* but the rhetoric/themes differ.
- **Runtime non-collusion** — the judge's drift intervention (§5.4) catches any live convergence; the orchestrator and tests assert no auto-agreement.

---

## 7. How skills enforce the per-turn rules (cross-references)

The skills *instruct*; other components *enforce*. The split:

| Rule | Instructed by (skill) | Enforced by (code) | Criterion |
|---|---|---|---|
| Rebut the opponent's last point | `skill_pro/con` §per-turn | `JudgeAgent.enforce` (`docs/PRD_judge_agent.md`) | A4 |
| Add exactly one new point | `skill_pro/con` themes | judge intervention on repetition | A2/A4 |
| Cite ≥1 web source | `skill_pro/con` | `protocol` citation validator + judge reject/retry (`docs/PRD_web_search.md`, `docs/PRD_ipc_protocol.md`) | A7 |
| ≤180 words/turn | `skill_pro/con` | `ProtocolMessage` word-count validator; judge rejects over-length | A10 |
| Never concede / stay on position | all three skills | judge drift intervention (§5.4) | A2 |
| PC, respectful, one-speaks-then-listens | all three skills | judge enforcement; orchestrator turn-taking | A10 |
| Real LLM output (no Python templates) | n/a — skills shape the live `claude -p` call | runtime (`docs/PRD_agent_base.md`) | A9 |
| Winner, differential score, no tie | `skill_judge` §5.3 | `agents/verdict.py` validation | A8 |
| Score persuasion, not truth | `skill_judge` §5.2 | judge scoring rubric | A8 |

A turn that violates a debater rule is **rejected and retried** (citation-less or over-length turns are not scored; the agent is asked to redo). This retry loop is owned by the Judge and Orchestrator, not by the skills — see `docs/PRD_judge_agent.md` and `docs/PRD_orchestrator.md`.

---

## 8. File format and authoring requirements

Each skill is a Markdown file under `src/cosmos77_ex02/skills/`, loaded as text and injected into `claude -p` via `--append-system-prompt` by `BaseAgent._render_prompt` (see `docs/PRD_agent_base.md`). Requirements:

- **F1** — First content line is `Description: …` (R-D1..R-D4 in §2.2).
- **F2** — Followed by the persona body: role, position (debaters), rhetorical strategy/theme list, the per-turn contract, and constraints.
- **F3** — English only (CLAUDE.md). No Arabic; no Hebrew in skill files (debate output standardizes on English).
- **F4** — No hardcoded debate values that already live in config. Topic, positions, `pings_per_side` (10), and `max_words_per_turn` (180) come from `config/setup.json` and are *injected* into context by the orchestrator/agent layer (rule 4, zero hardcoded config). A skill may *reference* "the configured word limit" but must not bake in a number that contradicts config.
- **F5** — No secrets, no API keys (rule 9; LLM auth is the `claude` CLI Max-subscription login, no key).
- **F6** — Each file kept concise to stay token-frugal under the Gatekeeper budget (`budget_usd_max` = 5.00, `per_call_usd_max` = 0.50; see `docs/PRD_gatekeeper.md`). The skill is sent on every call, so brevity directly reduces cost.

> **Note on the 150-line cap (rule 1):** the cap applies to `.py` files. Skill files are Markdown and are not subject to it, but the line-cap script (`scripts/check_line_cap.py`) only walks `src/**/*.py` and `tests/**/*.py`, so skills are excluded by construction.

---

## 9. Acceptance and verification

| ID | Requirement | Verification (Phase) |
|---|---|---|
| S-1 | Three skill files exist, non-empty: `skill_pro.md`, `skill_con.md`, `skill_judge.md` | `ls src/cosmos77_ex02/skills/`; unit test (Phase 4) |
| S-2 | Each begins with a distinct `Description:` line (R-D1..R-D4) | `diff <(head -1 skill_pro.md) <(head -1 skill_con.md)` → distinct; unit test asserts pairwise-distinct first lines (Phase 4) |
| S-3 | Pro = optimist/opportunity frame, argues NET POSITIVE, never concedes | content review + persona test (Phase 4) |
| S-4 | Con = skeptic/precaution frame (different strategy), argues NET NEGATIVE, never concedes — satisfies A2 | content review + persona test (Phase 4) |
| S-5 | Judge scores persuasion (4 dimensions), not truth; is position-neutral | content review; judge unit tests (Phase 4/7) |
| S-6 | Judge forbids ties; emits winner + differential score + turn-grounded justification (A8) | `verdict.py` validation test rejects equal scores (Phase 7) |
| S-7 | Judge intervenes on drift/agreement (A2/A4) | `JudgeAgent.enforce` drift test (Phase 7) |
| S-8 | All skills English-only; no hardcoded config; no secrets | content review; secret scan (Phase 11) |
| S-9 | Real session-1 transcript shows distinct strategies, mutual rebuttal, citations every turn, a no-tie verdict | `transcripts/session_001.json` audit (Phase 9/11); see `docs/PRD_orchestrator.md` |

---

## 10. Out of scope

- The Python agent classes that load these skills — see `docs/PRD_agent_base.md`, `docs/PRD_debater_agents.md`, `docs/PRD_judge_agent.md`.
- The citation tool and citation-validation rule — see `docs/PRD_web_search.md`.
- The JSON envelope, word-count validator, and routing — see `docs/PRD_ipc_protocol.md`.
- Adding a *new* persona/skill (e.g., a third debater or an alternate judge rubric) — covered as an extension path in `docs/PRD_extension_points.md` (subclass `BaseAgent` + add a skill file with a distinct Description line).
