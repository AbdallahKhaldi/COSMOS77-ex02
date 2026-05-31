# PRD — Extension Points

> **Scope.** This document specifies how `COSMOS77-ex02` ("AI Agent Debate", UOH-RL07 HW2) is extended *without rewriting the core*. It is the explicit closure of the HW1 grader's **"extensibility"** weakness (playbook §0.0). Four extension axes are covered, each with concrete steps, the exact files touched, and the tests/acceptance criteria that must stay green:
>
> 1. **Add a new agent** — subclass `BaseAgent` + ship a Skill.
> 2. **Add a new debate topic** — config only, *zero code*.
> 3. **Add a new LLM backend** — implement the runtime interface (GLM / Gemini / Codex / OpenAI).
> 4. **Add a new judge rubric** — swap the Judge Skill + extend `score_turn` weights.
>
> Cross-references: see `docs/PRD_agent_base.md`, `docs/PRD_debater_agents.md`, `docs/PRD_judge_agent.md`, `docs/PRD_skills.md`, `docs/PRD_orchestrator.md`, `docs/PRD_ipc_protocol.md`, and the ADRs in `docs/PLAN.md` (ADR-001..ADR-008). These extension points are also surfaced to graders via the README "How to extend" section (playbook §3 Phase 10, item 13).

---

## 1. Design intent and the contracts that make extension cheap

Extensibility is not a feature bolted on at the end; it is the consequence of three architectural decisions taken in `docs/PLAN.md` and enforced repo-wide:

- **A single SDK seam (rule 2).** Every external caller — the terminal menu (`src/cosmos77_ex02/cli/menu.py`), the CLI entry (`src/cosmos77_ex02/cli/main.py`), the orchestrator entry, and any future consumer — talks only to `class SDK` in `src/cosmos77_ex02/sdk/sdk.py`. New behaviour is added *behind* the SDK; callers do not change.
- **Polymorphism over conditionals (rule 3).** Agents form a class hierarchy (`BaseAgent` → `DebaterAgent` → `ProAgent`/`ConAgent`; `JudgeAgent`). New agents are *new subclasses*, not new `if role == ...` branches.
- **Config-driven everything (rule 4).** Topic, positions, ping count, timeouts, the budget cap, allowed tools, the CLI path, and log rotation all live in `config/setup.json`, `config/gatekeeper.json`, and `config/logging_config.json`, read through `src/cosmos77_ex02/shared/config.py` via dot-path access (e.g. `cfg.get("debate.pings_per_side")`). Changing the *debate* never means changing *code*.

The four "stable contracts" an extension must respect are:

| Contract | Defined in | What an extension must NOT break |
|---|---|---|
| **Runtime interface** | `src/cosmos77_ex02/runtime/claude_cli.py` (`ClaudeCliRuntime.invoke(...) -> LlmResult`) | Must return an `LlmResult` carrying `text`, `cost_usd`, `input_tokens`, `output_tokens`, `is_error`, `raw` so the Gatekeeper can meter it. |
| **Agent contract** | `src/cosmos77_ex02/agents/base.py` (`BaseAgent.act(context) -> ProtocolMessage`) | Must emit a schema-valid `ProtocolMessage`; debaters must rebut + add a point + cite ≥1 source within `max_words_per_turn`. |
| **Protocol envelope** | `src/cosmos77_ex02/protocol/message.py` (`ProtocolMessage`) | Routing stays child → judge → child (A5); messages stay pydantic-validated JSON (A6). |
| **Gatekeeper** | `src/cosmos77_ex02/shared/gatekeeper.py` (`Gatekeeper.guard(...)`) | Every LLM call routes through `guard`; spend hard-stops at `budget_usd_max = 5.00` (rule 13). |

Any extension that honours these four contracts inherits — for free — the watchdog/restart logic, the FIFO logs (20 files × 500 lines), the cost budget, the JSON transcript, and the no-tie verdict. That is the whole point.

---

## 2. Extension axis A — Add a new agent

**Use case.** A third debater stance (e.g. a "Moderate / nuanced" position), a dedicated *fact-checker* agent that flags an opponent's unsupported claims, or a *summarizer* agent. The fixed three-process layout (Judge father + Pro + Con; see `docs/PRD_orchestrator.md`) stays intact for the graded session; a new agent is an opt-in extra process the orchestrator can spawn.

### 2.1 Pattern

Agents are polymorphic. The base class already centralises prompt rendering, the metered LLM invocation, and message construction (per `docs/PRD_agent_base.md`):

```python
# src/cosmos77_ex02/agents/base.py (existing contract)
class BaseAgent(ABC):
    def __init__(self, role: str, skill_text: str,
                 runtime: ClaudeCliRuntime, gatekeeper: Gatekeeper) -> None: ...
    @abstractmethod
    def act(self, context: dict) -> ProtocolMessage: ...
    def _render_prompt(self, context: dict) -> str: ...   # shared
    def _invoke(self, system_prompt: str, user_prompt: str) -> LlmResult: ...  # always via Gatekeeper.guard
    def _to_message(self, text: str, *, turn_type: str, ...) -> ProtocolMessage: ...  # shared
```

A new agent overrides only `act()` and supplies its own Skill file; timeout handling, cost accounting, and message emission are inherited (rule 3 — no duplication).

### 2.2 Concrete steps

1. **Write the Skill** `src/cosmos77_ex02/skills/skill_factchecker.md` — a one-line `Description:` selector on line 1 (this drives skill selection; see `docs/PRD_skills.md`) followed by the persona. English-only, PC language (A10). It must be *textually distinct* from the existing three skill descriptions (the Phase-4 test diffs line 1 of each skill file).
2. **Subclass the agent** in `src/cosmos77_ex02/agents/factchecker.py` (≤120 lines, rule 1):
   ```python
   class FactCheckerAgent(BaseAgent):
       """Flags an opponent's unsupported or contradicted claims; persuasiveness-neutral."""
       def act(self, context: dict) -> ProtocolMessage:
           prompt = self._render_prompt(context)
           result = self._invoke(self.skill_text, prompt)   # metered via Gatekeeper
           return self._to_message(result.text, turn_type="rebuttal", ...)
   ```
3. **Register it in the factory** `src/cosmos77_ex02/agents/factory.py` — add the `role -> class` mapping so `build_agent("factchecker", cfg)` resolves it. Unknown roles still raise (existing contract).
4. **Allow the role in the protocol** `src/cosmos77_ex02/constants.py` — extend `ROLES`, currently `("judge", "pro", "con")`. The routing validator in `src/cosmos77_ex02/protocol/routing.py` must keep the child → judge → child invariant (A5): a new *debater-like* agent may send only to `"judge"` and receive only from `"judge"`; never child → child.
5. **Spawn it (optional process)** `src/cosmos77_ex02/orchestration/orchestrator.py` — if the agent participates in the live loop, add it to the spawned-process set alongside judge/pro/con (`process_agent.py` already runs *one arbitrary agent* per process with inbound/outbound `multiprocessing.Queue`s, so no new process plumbing is needed). The watchdog (`watchdog.py`) monitors heartbeats generically, so restart/keep-alive (`watchdog_keepalive_seconds = 15`, `max_restarts_per_agent = 3`) covers the new process for free.
6. **Surface it via the SDK** `src/cosmos77_ex02/sdk/sdk.py` — the menu/CLI reach the agent only through `SDK.build_agent(role)`; no new public surface is required unless you add a dedicated menu option.

### 2.3 Files touched

| File | Change |
|---|---|
| `src/cosmos77_ex02/skills/skill_<name>.md` | **new** Skill (distinct Description line) |
| `src/cosmos77_ex02/agents/<name>.py` | **new** `BaseAgent` subclass (≤120 lines) |
| `src/cosmos77_ex02/agents/factory.py` | add `role -> class` mapping |
| `src/cosmos77_ex02/constants.py` | extend `ROLES` |
| `src/cosmos77_ex02/protocol/routing.py` | allow the new role under the child→judge→child rule (if a debater) |
| `src/cosmos77_ex02/orchestration/orchestrator.py` | spawn/sequence the extra process (if live) |
| `tests/unit/test_agents/test_<name>.py` | **new** happy + error path (rule 6) |

### 2.4 Acceptance / tests to keep green

- A2 (distinct Skills), A3/A4 (ping count + mutual rebuttal unchanged for the graded pair), A5 (routing through the father), A13 (OOP + inheritance — the new subclass *is* the evidence).
- New unit tests must mock the runtime and the Gatekeeper (rule 6, A14): assert the agent loads the right skill, emits a valid `ProtocolMessage`, and that a missing-citation turn (for debater-like agents) is flagged.
- Coverage on `agents/` must stay ≥90% (Phase 4 target; repo floor is 85%, rule 7).

---

## 3. Extension axis B — Add a new debate topic (config only, no code)

**Use case.** Re-run the system on any motion — "Should AI development be paused?", "Is remote work a net positive for organisations?" — without touching Python. This is the cleanest demonstration of rule 4 (zero hardcoded config).

### 3.1 What lives in config

The entire debate definition is the `debate` block of `config/setup.json`:

```json
"debate": {
  "topic": "Is social media a net positive for society?",
  "pro_position": "Social media is a NET POSITIVE for society.",
  "con_position": "Social media is a NET NEGATIVE for society.",
  "pings_per_side": 10,
  "max_words_per_turn": 180,
  "require_citation_per_turn": true,
  "language": "english"
}
```

`ProAgent` and `ConAgent` inject `pro_position` / `con_position` into their prompts; the Judge Skill receives only the `topic` and the rules of the game — it never learns the "right answer" (anti-bias, see `docs/PRD_judge_agent.md`). Because the position strings are config, the *same* `skill_pro.md` / `skill_con.md` personas (evidence-driven optimist vs. critical skeptic) adapt to the new motion automatically.

### 3.2 Concrete steps

1. Edit `config/setup.json` → `debate.topic`, `debate.pro_position`, `debate.con_position`. Keep positions genuinely opposed so the debate does not collapse into agreement (A2/A4).
2. (Optional) Tune `debate.pings_per_side` (default `10`; the spec permits `5` in budget mode — playbook §0) and `debate.max_words_per_turn` (default `180`). Keep `require_citation_per_turn: true` to preserve A7, and `language: "english"` to preserve the English-only rule (rule 9 / playbook §0).
3. Bump the config `version` if the schema (not just values) changes; `src/cosmos77_ex02/shared/version.py::validate_config_version()` checks it on load.
4. Run: `uv run cosmos77-debate run`, or use terminal-menu option **[2] Set topic & positions** (see `docs/PRD_terminal_menu.md`), which writes the same keys through `SDK.set_topic(...)`.

### 3.3 Files touched

| File | Change |
|---|---|
| `config/setup.json` | edit `debate.topic`, `debate.pro_position`, `debate.con_position` (and optionally `pings_per_side`, `max_words_per_turn`) |

**No `.py` file changes. No new tests.** This is the explicit proof of the "config only" promise. The existing config-loader tests (`tests/unit/test_shared/test_config.py`) already cover dot-path reads; the new topic flows through unchanged. New transcripts are written to `transcripts/session_NNN.json` (the graded session-1 file stays committed).

> **Guardrail.** Topics must remain answerable with publicly searchable evidence (the debaters *must* cite ≥1 web source per turn, A7) and must keep PC, respectful framing (A10). A topic with no searchable sources would cause repeated citation-less turns to be rejected and retried, burning Gatekeeper budget.

---

## 4. Extension axis C — Add a new LLM backend

**Use case.** The HW1 "cost/dependency" critique pushes toward *backend independence*. The shipped backend is the `claude` CLI headless (`claude -p --output-format json --allowedTools WebSearch`) authenticated via the Max subscription with **no API key** (ADR-001, playbook §0). A new backend — GLM, Gemini, Codex/OpenAI, or a local model — plugs in by implementing the same runtime interface, so the agents, orchestrator, protocol, and Gatekeeper are untouched.

### 4.1 The runtime interface (the contract)

The current backend is `ClaudeCliRuntime` in `src/cosmos77_ex02/runtime/claude_cli.py`, split into `runtime/argv.py` (builds argv) and `runtime/parse.py` (parses JSON) to respect the 150-line cap. Its single public method and return type are the contract every backend must satisfy:

```python
@dataclass
class LlmResult:
    text: str
    cost_usd: float
    input_tokens: int
    output_tokens: int
    session_id: str | None
    is_error: bool
    raw: dict

class ClaudeCliRuntime:  # the reference implementation
    def invoke(self, system_prompt: str, user_prompt: str, *,
               allowed_tools: list[str], timeout_s: int) -> LlmResult: ...
```

The non-negotiable obligations of any `invoke(...)`:

- Return a populated `LlmResult`. `cost_usd` / token counts feed the **Gatekeeper** — if a backend cannot report cost, map it to `0.0` and log a warning (this is exactly what `runtime/parse.py` does today for a missing cost field), but the Gatekeeper's USD cap then under-counts, so document it.
- Honour `timeout_s` (`per_call_timeout_seconds = 120` from `config/setup.json` runtime block) and raise `RuntimeTimeout` on overrun; raise `RuntimeError` on backend error / non-zero exit.
- Provide a web-search capability for `allowed_tools = ["WebSearch"]` (A7). If the backend lacks native search, route through the fallback `WebSearchTool` in `src/cosmos77_ex02/tools/` (see `docs/PRD_web_search.md`) so debaters can still cite ≥1 source.
- Never call a live network/subprocess in tests (rule 6, A17): the new backend's tests mock its transport exactly as `tests/unit/test_runtime/` mocks `subprocess.run`.

### 4.2 Concrete steps (formalising the seam)

1. **Extract a Protocol** `src/cosmos77_ex02/runtime/base.py` — declare a `typing.Protocol` (or ABC) `LlmRuntime` with the `invoke(...) -> LlmResult` signature above. `ClaudeCliRuntime` already satisfies it structurally; this just names the contract for new backends and the type checker.
2. **Implement the backend**, e.g. `src/cosmos77_ex02/runtime/gemini_cli.py` or `runtime/openai_runtime.py` (≤150 lines; split argv/parse helpers if needed). It translates `(system_prompt, user_prompt, allowed_tools, timeout_s)` into the vendor call and maps the vendor response (text + usage/cost) onto `LlmResult`. API-key backends read their key from `.env` via the Config loader — `.env.example` documents the placeholder (`WEB_SEARCH_API_KEY` already exists there as the search-fallback precedent); never commit a real key (rule 9, A11).
3. **Add a runtime selector** in `config/setup.json` runtime block, e.g. `"backend": "claude_cli"` (default) with options `claude_cli | gemini | openai | glm`, plus any backend-specific keys (model name, base URL). A small `runtime/factory.py::build_runtime(cfg) -> LlmRuntime` reads it and returns the right instance — the *only* place backend selection branches (rule 3).
4. **Wire through the SDK only.** `src/cosmos77_ex02/sdk/sdk.py` constructs the runtime via `build_runtime(cfg)` and passes it to `build_agent(role, cfg, runtime)`. Agents already receive the runtime by injection (`BaseAgent.__init__`), so no agent code changes.
5. **Keep the Gatekeeper in the loop.** Because agents invoke through `BaseAgent._invoke()` → `Gatekeeper.guard()`, the new backend's `cost_usd` is metered and the `budget_usd_max = 5.00` hard stop (`config/gatekeeper.json`) applies unchanged.

### 4.3 Files touched

| File | Change |
|---|---|
| `src/cosmos77_ex02/runtime/base.py` | **new** `LlmRuntime` Protocol/ABC (names the contract) |
| `src/cosmos77_ex02/runtime/<backend>.py` | **new** backend implementing `invoke(...) -> LlmResult` |
| `src/cosmos77_ex02/runtime/factory.py` | **new/edit** `build_runtime(cfg)` selector |
| `config/setup.json` | add `runtime.backend` (+ backend keys) |
| `.env.example` | add placeholder for backend API key (if not key-less) |
| `src/cosmos77_ex02/sdk/sdk.py` | construct runtime via `build_runtime(cfg)` |
| `tests/unit/test_runtime/test_<backend>.py` | **new** mocked happy + error + timeout paths |

### 4.4 ADR linkage and acceptance

This axis is the realisation of **ADR-001** (Claude CLI headless chosen as the *default*, alternatives documented) in `docs/PLAN.md`. It keeps A9 (real LLM debate, never Python string templates) and A11 (Gatekeeper, timeouts) intact because the metered, timed, web-searching contract is mandatory for every backend. Coverage on `runtime/` must stay ≥90% (Phase 3 target), and the suite must never make a live call (A14/rule 17).

---

## 5. Extension axis D — Add a new judge rubric

**Use case.** Re-weight what "persuasiveness" means — e.g. a rubric that prizes *evidence quality* over *rhetorical force*, an academic-debate (BP-style) rubric, or a "novice-friendly clarity-first" rubric. The judge scores **persuasiveness only — never factual truth** (lies are allowed and must be caught by the opponent, A8); a new rubric changes the *weights and criteria*, not that principle, and the **no-tie** rule is immutable.

### 5.1 What a rubric is, in this system

The rubric has two coupled parts (see `docs/PRD_judge_agent.md`):

1. **The Judge Skill** `src/cosmos77_ex02/skills/skill_judge.md` — natural-language instructions telling the LLM judge *what to value* (clarity, evidence use, rebuttal quality, rhetorical force) and the rules of the game. It explicitly forbids ties and forbids scoring on factual truth, and instructs the judge to intervene if a debater drifts into agreeing.
2. **The scoring code** `JudgeAgent.score_turn(turn)` and `JudgeAgent.verdict(transcript) -> Verdict` in `src/cosmos77_ex02/agents/judge.py`, plus the `@dataclass Verdict {winner, pro_score, con_score, justification, decided_at}` in `src/cosmos77_ex02/agents/verdict.py` whose validation **forbids equal scores / "tie"** (A8).

### 5.2 Two extension flavours

**(a) Rubric text only (no code).** To re-weight emphasis qualitatively, edit `skill_judge.md` (or add `skill_judge_evidence_first.md`) and point the judge at it. Keep the four invariants the Skill must always state: persuasiveness-not-truth, mandatory winner, differential score, justification grounded in specific turns. This is the lightest change and touches one file.

**(b) Structured rubric weights (config + small code).** To make weights *tunable and testable*, add a `judge` block to `config/setup.json`, e.g.:

```json
"judge": {
  "rubric": "default",
  "weights": { "clarity": 0.25, "evidence": 0.30, "rebuttal": 0.30, "rhetoric": 0.15 }
}
```

Then have `JudgeAgent.score_turn(...)` read the weights via the Config loader and apply them when aggregating the four sub-scores. `verdict(...)` keeps its tie-break: if aggregate scores are close, **break by rebuttal quality** and emit unequal scores (e.g. Pro 80 / Con 73) — never a tie.

### 5.3 Concrete steps

1. **Author the rubric Skill** `src/cosmos77_ex02/skills/skill_judge_<name>.md` (or edit the existing one). Distinct Description line; English; PC. Restate the immutable invariants (no tie, persuasiveness-only, justification per specific turns).
2. **(Flavour b) Add config** `config/setup.json` → `judge.rubric` + `judge.weights`. Weights should sum to 1.0; validate on load.
3. **Read weights in code** `src/cosmos77_ex02/agents/judge.py` — `score_turn` pulls `cfg.get("judge.weights")`; default to the current implicit weights if the block is absent (backward-compatible, rule 4 exception: default-arg values only).
4. **Select the skill** — either point `JudgeAgent` at the new skill file by config key `judge.rubric`, or via `build_agent("judge", cfg)` in `factory.py`.
5. **Keep the verdict contract** — `verdict.py` validation that bans equal scores is untouched; this is what mechanically guarantees A8.

### 5.4 Files touched

| File | Change |
|---|---|
| `src/cosmos77_ex02/skills/skill_judge_<name>.md` | **new/edit** rubric persona (invariants restated) |
| `config/setup.json` | **add** `judge.rubric` + `judge.weights` (flavour b) |
| `src/cosmos77_ex02/agents/judge.py` | read weights in `score_turn`; rubric selection (flavour b) |
| `src/cosmos77_ex02/agents/factory.py` | bind judge to the chosen rubric/skill (if selected by role/config) |
| `tests/unit/test_agents/test_judge.py`, `test_verdict.py` | extend: new weights produce a winner; **no tie** ever; justification non-empty and references turns |

### 5.5 Acceptance to keep green

- **A8 — no tie:** `verdict.py` must still raise on equal scores; the test asserting a winner with unequal scores and a non-empty, turn-referencing justification must pass under the new weights.
- **A4 / A7 enforcement** in `JudgeAgent.enforce(...)` (citation-less, over-length, non-rebutting, or drifting-into-agreement turns are rejected/intervened) is rubric-independent and must remain green.
- Coverage on `judge`/`verdict` stays ≥90% (Phase 7 target).

---

## 6. Summary matrix

| Axis | Code change? | Primary files | Key acceptance criteria preserved |
|---|---|---|---|
| **A. New agent** | Yes (subclass + Skill + factory + ROLES) | `agents/<name>.py`, `skills/skill_<name>.md`, `agents/factory.py`, `constants.py`, `protocol/routing.py` | A2, A4, A5, A13 |
| **B. New topic** | **No** (config only) | `config/setup.json` (`debate` block) | A2, A4, A7, A10 |
| **C. New LLM backend** | Yes (runtime impl + factory + selector) | `runtime/<backend>.py`, `runtime/base.py`, `runtime/factory.py`, `config/setup.json`, `sdk/sdk.py` | A7, A9, A11, A14 |
| **D. New judge rubric** | Light (Skill ± weights/code) | `skills/skill_judge_<name>.md`, `config/setup.json` (`judge` block), `agents/judge.py`, `agents/verdict.py` | A4, A7, A8 |

## 7. Invariants every extension must preserve (the do-not-break list)

1. **Three-process model + child → judge → child routing** (A1, A5) — children never talk directly; the Judge father relays every message.
2. **JSON + pydantic protocol** (A6) — extensions exchange `ProtocolMessage`, validated and logged.
3. **Mandatory web-search citation per debater turn** (A7) — citation-less turns are rejected and retried (`require_citation_per_turn = true`).
4. **No tie, ever** (A8) — the Judge always declares a differential winner with a written, turn-grounded justification.
5. **Gatekeeper budget** (rule 13, A11) — every LLM call routes through `Gatekeeper.guard`; spend hard-stops at `budget_usd_max = 5.00`.
6. **The hard rules** — 150 lines/.py (rule 1), SDK-only seam (rule 2), no duplication (rule 3), config-driven (rule 4), uv-only (rule 5), TDD with all I/O mocked (rule 6), coverage ≥85% (rule 7), zero ruff (rule 8), no secrets (rule 9), English only.

## 8. Where this is referenced

- **`docs/PLAN.md`** — ADR-001 (backend choice; axis C), and the risk-register mitigations for "agents auto-agreeing" (axis D rubric/enforce) and "budget overrun" (Gatekeeper across all axes) link back here.
- **`README.md` "How to extend" section** (playbook §3, Phase 10 item 13) — links this document and summarises the four axes for the grader.
- **`docs/ACCEPTANCE.md`** (Phase 11) — maps A1–A15 to tests/artifacts; the invariants in §7 are the cells an extension must not turn red.
