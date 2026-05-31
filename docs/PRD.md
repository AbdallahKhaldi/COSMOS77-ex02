# PRD — COSMOS77-ex02: AI Agent Debate (UOH-RL07 HW2)

> **Status:** Approved for build (Phase 1 artifact). **Version:** 1.00. **Owners:** Abdallah Khaldi, Tasneem Natour.
> **Scope of this document:** the Product Requirements for the *whole* assignment. Per-mechanism PRDs decompose the design further — see `docs/PRD_agent_base.md`, `docs/PRD_judge_agent.md`, `docs/PRD_debater_agents.md`, `docs/PRD_skills.md`, `docs/PRD_ipc_protocol.md`, `docs/PRD_orchestrator.md`, `docs/PRD_watchdog.md`, `docs/PRD_gatekeeper.md`, `docs/PRD_logging.md`, `docs/PRD_web_search.md`, `docs/PRD_terminal_menu.md`, and `docs/PRD_extension_points.md`. The architecture, C4 diagrams, sequence diagram, and ADRs live in `docs/PLAN.md`; the granular work breakdown (≥600 items) lives in `docs/TODO.md`. The 17 binding global rules are in `CLAUDE.md`; the acceptance criteria A1–A15 are defined in `../CLAUDE_CODE_PLAYBOOK.md` §1.5 and mapped below.

## 1. Context & Rationale

This product is **HW2 — "AI Agent Debate"** for **UOH-RL07 "Vibe Coding & AI Agents"** (Dr. Yoram Segal). The deliverable is a runnable Python program that stages a **Pro vs Con debate adjudicated by a third agent**, on the config-driven topic **"Is social media a net positive for society?"** (`config/setup.json` → `debate.topic`). The Pro side argues that **social media is a NET POSITIVE for society**; the Con side argues that it is a **NET NEGATIVE** (`debate.pro_position` / `debate.con_position`).

**Why a 3-agent debate, and why now.** The course's central pedagogical move is the shift from **Prompt Engineering** (crafting one clever prompt for one model) to **Context Engineering** (orchestrating *what each agent sees, when, and from whom* across a multi-agent system). A single-prompt summarizer demonstrates neither. A three-process debate does: it forces us to **Select** the right slice of conversational state into each agent's prompt, **Write/evict** old turns so the context window stays small and cheap, and route every message through a controlling parent. The Judge (father process) owns turn-taking, anti-collusion intervention, and the final verdict; the two debaters are stateless workers that receive only the context the orchestrator hands them. This is Context Engineering made concrete — the orchestrator's job *is* context curation (detailed in `docs/PRD_orchestrator.md`).

**Why this exact shape.** The substance graded here is *orchestration that actually works*: three real OS processes (not threads, not a single chat), a real LLM debate with genuine disagreement, mandatory web-search citations, JSON messages routed child → judge → child, a watchdog that restarts a stalled or dead process, and a judge that declares a justified winner with **no tie, ever**. The engineering layers that wrap it — Gatekeeper cost meter, SDK single entry point, FIFO structured logs, terminal menu, config-driven everything, OOP with a committed class diagram — are first-class graded requirements, not decoration. A beautiful set of documents wrapped around a debate that hangs, ties, or agrees with itself fails the assignment; the grader clones the repo and runs `uv run cosmos77-debate run`.

## 2. Stakeholders

| Stakeholder | Role / interest | What they need from this product |
|---|---|---|
| **Grader (automated + human review)** | Clones the repo, runs the system, walks the acceptance matrix (A1–A15) and the 17 rules. | A debate that runs end-to-end to a no-tie verdict; reproducible env (`uv sync`); committed `transcripts/session_001.json`; README evidence; green CI. |
| **Dr. Yoram Segal (lecturer / course owner)** | Owns UOH-RL07 grading philosophy; values cost awareness, extensibility, and analysis-over-numbers. | Demonstrated Context Engineering, a justified verdict (not a number dump), a cost section, and documented extension points. Added as repo collaborator (`rmisegal@gmail.com`) before Moodle. |
| **Abdallah Khaldi (student partner, primary author)** | Drives Phases 0–12, owns repo identity, cover PDF, submission. | A clear, phase-by-phase build plan; both authors visible in `git shortlog -sn`. |
| **Tasneem Natour (student partner, co-author)** | Takes ownership of designated phases (switches `git user.name/email` so both authors appear). | The same build plan; her commits attributed; separate Moodle upload (per-student timer). |
| **Operator / end user (running the program)** | Invokes the terminal menu or CLI to start, configure, and inspect a debate. | One command to launch; readable verdict, cost report, and log tail. |
| **Maintainer / future extender** | Adds a new agent, topic, backend, or rubric later. | Stable SDK + factory + runtime interface; `docs/PRD_extension_points.md`. |

## 3. User Stories

**End user / operator**
- *As a user, I run one command (`uv run cosmos77-debate run`) and watch a Pro vs Con debate, routed through a judge, that ends in a single justified verdict — never a tie.*
- *As a user, I open a keyboard-driven terminal menu and choose: [1] run debate, [2] set topic & positions, [3] set pings per side, [4] view last verdict, [5] tail logs, [6] cost report, [7] show architecture diagram path, [0] quit — every option backed by the SDK* (see `docs/PRD_terminal_menu.md`).
- *As a user, I can change the debate topic, the two positions, and the pings per side via `config/setup.json` (or menu option [2]/[3]) without editing any Python.*
- *As a cost-conscious user, I see a per-run cost report (total USD, tokens, cost per ping) and trust the run aborts cleanly before it exceeds the `$5.00` budget cap.*

**Operator / reliability**
- *As an operator, if a debater process stalls past `watchdog_keepalive_seconds` (15s) or dies, the watchdog kills and restarts it (up to `max_restarts_per_agent` = 3), replaying its last context so the debate continues rather than hanging.*
- *As an operator, I can audit the entire run from FIFO structured JSON-lines logs (20 files × 500 lines) under `logs/`.*

**Grader**
- *As the grader, I clone the repo, run `uv sync`, and reproduce a full debate; I confirm three separate OS processes, every message routed child → judge → child, ≥10 pings/side, a citation on every debater turn, and a no-tie justified verdict.*
- *As the grader, I read the README first and find: the full JSON dialogue of session 1, screenshots, the exact Skills, a cost analysis, and a self-assessment against every rule and criterion* (see Phase 10; A15).
- *As the grader, I verify each of A1–A15 maps to a passing test or a committed artifact via `docs/ACCEPTANCE.md`.*

**Maintainer**
- *As a maintainer, I add a new debater by subclassing `BaseAgent` + a Skill file, a new topic by editing config only, and a new LLM backend by implementing the runtime interface — guided by `docs/PRD_extension_points.md`.*

## 4. Functional Requirements (mapped to Acceptance Criteria A1–A15)

Each functional requirement (FR) is testable and is satisfied by a phase artifact and/or a test. Acceptance criteria definitions are in `../CLAUDE_CODE_PLAYBOOK.md` §1.5; module/phase mapping follows that document's coverage matrix.

| FR | Requirement (pinned to configured values) | Maps to | Primary artifact / phase |
|---|---|---|---|
| **FR-1** | Run the Judge (father), Pro, and Con each as a **separate OS process**; debaters never share a process. Communication is IPC (multiprocessing Queues). | **A1** | `orchestration/process_agent.py`, `orchestration/orchestrator.py` (Phase 6); `docs/PRD_orchestrator.md` |
| **FR-2** | Pro and Con load **different** Skill files (`skill_pro.md` vs `skill_con.md`) with distinct personas/rhetoric; the Judge loads `skill_judge.md` and does **not** know the "right answer". | **A2** | `skills/skill_pro.md`, `skills/skill_con.md`, `skills/skill_judge.md` (Phase 4); `docs/PRD_skills.md` |
| **FR-3** | Run **≥10 pings per side**, config-driven via `debate.pings_per_side = 10`. A ping = one argument plus the opponent's counter-argument. | **A3** | `orchestration/loop.py`, `config/setup.json` (Phase 6) |
| **FR-4** | Each debater turn must **explicitly rebut** the opponent's previous argument (no parallel monologues); the Judge rejects non-rebutting turns. | **A4** | `JudgeAgent.enforce`, debater prompts (Phase 7); `docs/PRD_debater_agents.md` |
| **FR-5** | **Every** message routes **child → judge → child**; debaters may only send to `judge` and receive from `judge`. Child→child traffic is rejected by the routing validator. | **A5** | `protocol/routing.py`, orchestrator loop (Phases 5–6); `docs/PRD_ipc_protocol.md` |
| **FR-6** | All inter-process messages are **JSON, schema-validated with pydantic**, logged, and monitorable. Envelope: `{msg_id, ts, sender, recipient, role, ping_no, turn_type, content, citations[], word_count, tokens, cost_usd}`. | **A6** | `protocol/message.py` (Phase 5); `docs/PRD_ipc_protocol.md` |
| **FR-7** | Each debater must use a web-search tool and **cite ≥1 source per argument** (`debate.require_citation_per_turn = true`). A turn with no citation is **rejected and retried**. Runtime passes `--allowedTools WebSearch` (`runtime.allowed_tools = ["WebSearch"]`). | **A7** | `runtime/claude_cli.py`, citation enforcement in Judge, `WebSearchTool` fallback (Phases 3, 4, 7); `docs/PRD_web_search.md` |
| **FR-8** | The Judge **must declare a winner** with a **differential score** (e.g., Pro 80 / Con 73) and a written justification grounded in specific turns. **No tie ever**; equal scores / "tie" are forbidden by validation. Scoring is on **persuasiveness** (clarity, evidence use, rebuttal quality, rhetorical force), **not** factual truth — lies are allowed and should be caught by the opponent. | **A8** | `agents/verdict.py`, `JudgeAgent.verdict` (Phase 7); `docs/PRD_judge_agent.md` |
| **FR-9** | All arguments come from the **LLM** (`claude -p --output-format json`), never fabricated by Python string templates. | **A9** | `runtime/claude_cli.py`, live integration test (Phases 3, 6) |
| **FR-10** | Enforce **PC, respectful, turn-taking** language: one speaks, finishes, the other listens; enforce `debate.max_words_per_turn = 180`. Over-length turns are rejected/retried. | **A10** | Skills + `JudgeAgent.enforce` (Phases 4, 7) |
| **FR-11** | Provide engineering must-haves: per-call timeout (`runtime.per_call_timeout_seconds = 120`); Watchdog keep-alive (`watchdog_keepalive_seconds = 15`, `max_restarts_per_agent = 3`); Gatekeeper budget cap; SDK layer; FIFO logs (20×500); zero hardcoded params; `.env.example` only. | **A11** | `watchdog.py`, `gatekeeper.py`, `logging_setup.py` + `fifo_handler.py`, `config/`, `sdk/sdk.py` (Phases 0, 2, 6); `docs/PRD_watchdog.md`, `docs/PRD_gatekeeper.md`, `docs/PRD_logging.md` |
| **FR-12** | Operable from a **keyboard-driven terminal menu** with the 8 options listed in §3; every option calls an SDK method. GUI is optional and out of scope (§7). | **A12** | `cli/menu.py`, `cli/main.py` (Phase 8); `docs/PRD_terminal_menu.md` |
| **FR-13** | **OOP with inheritance, no duplication** (`BaseAgent → DebaterAgent → ProAgent/ConAgent`, `JudgeAgent`), plus committed **class + sequence diagrams** rendered to PNG. | **A13** | `agents/*`, `docs/diagrams/architecture.mmd`, `docs/diagrams/sequence.mmd`, `assets/*.png` (Phases 4, 9); diagrams in `docs/PLAN.md` |
| **FR-14** | **Reproducible env**: `uv` + `pyproject.toml` + `uv.lock`; the `claude` CLI is documented as an external prerequisite (not a pip dependency). | **A14** | `pyproject.toml`, `uv.lock`, `.python-version`=3.11 (Phase 0) |
| **FR-15** | **README evidence**: screenshots, the exact prompts/Skills, the **full JSON dialogue of session 1**, a cost section, and a self-assessment. | **A15** | `README.md`, `transcripts/session_001.json`, `assets/` (Phases 9–10) |

## 5. Non-Functional Requirements

- **NFR-1 — Robustness / no hang.** The system never deadlocks or hangs indefinitely. Every `claude -p` call is bounded by `per_call_timeout_seconds = 120`. The Watchdog monitors per-process heartbeats; if a process stalls past `watchdog_keepalive_seconds = 15` or dies, it is terminated and respawned up to `max_restarts_per_agent = 3`, replaying the last context so the debate resumes. Every restart is logged. See `docs/PRD_watchdog.md`. (Supports A11.)
- **NFR-2 — Cost ceiling.** Every LLM/agent invocation routes through the Gatekeeper (`shared/gatekeeper.py`), which reads `total_cost_usd`/`usage` from the `claude -p` JSON, accumulates spend, **warns at `warn_at_fraction = 0.8`**, enforces `per_call_usd_max = 0.50`, and **hard-stops** (`hard_stop = true`) cleanly at `budget_usd_max = 5.00`. A budget trip aborts the debate gracefully (catchable `BudgetExceeded`), never crashes. See `docs/PRD_gatekeeper.md`. (Supports A11; closes the HW1 cost-awareness gap.)
- **NFR-3 — Reproducibility.** A fresh clone + `uv sync` reproduces the environment; Python pinned to 3.11; `uv.lock` committed and `uv lock --check` passes. The `claude` CLI on a Max subscription is the only external prerequisite, documented in the README quickstart. Tests are deterministic (seeded RNG; all subprocess/network I/O mocked). (Supports A14.)
- **NFR-4 — Testability.** TDD red→green→refactor; every public function/class has at least one happy-path and one error-path test; **all** subprocess/LLM/network I/O is mocked (no live `claude` calls in the suite); **coverage ≥ 85%** (`fail_under = 85`). The SDK is usable programmatically so an agent can drive and debug the system headlessly. (Supports A14, A15; satisfies rules 6, 7, 17.)
- **NFR-5 — English-only output.** All code, comments, docs, Skills, and debate output are in **English** (`debate.language = "english"`); Arabic is forbidden by the spec, Hebrew is allowed only on the cover PDF's name fields. (Satisfies rule "English only".)
- **NFR-6 — Security / no secrets.** No keys, tokens, or session credentials in the repo. LLM auth is the `claude` CLI Max-subscription login — there is **no API key**. Only `.env.example` placeholders are committed; `.env` is gitignored. The Gatekeeper's `scrub()` helper redacts anything resembling a key/token before logging. (Satisfies rule 9; cyber layer.)
- **NFR-7 — Maintainability / extensibility.** 150-line hard cap per `.py` file; single SDK entry point; OOP base classes and a `build_agent` factory; a runtime interface that admits alternative backends. Extension paths documented in `docs/PRD_extension_points.md`. (Closes the HW1 extensibility gap; satisfies rules 1, 2, 3.)
- **NFR-8 — Auditability.** Structured FIFO JSON-lines logs (20 files × 500 lines, config-driven) capture agent calls, messages, costs, restarts, and the verdict, so the entire run is reconstructible from `logs/`. See `docs/PRD_logging.md`.

## 6. Key Performance Indicators (KPIs)

The build is "done right" when **all** of the following hold simultaneously:

| KPI | Target | Source of truth |
|---|---|---|
| Pings per side | **≥ 10** | `debate.pings_per_side = 10`; orchestrator loop count in `session_001.json` |
| Ties | **0 (no tie ever)** | `Verdict` validation forbids equal scores; `JudgeAgent.verdict` |
| Citations per debater turn | **≥ 1** | `require_citation_per_turn = true`; per-message `citations[]` non-empty |
| Test coverage | **≥ 85%** | `pytest --cov-fail-under=85` |
| ruff issues | **0** | `uv run ruff check .` |
| TODO granularity | **≥ 600 items** | `docs/TODO.md` (`grep -c '^T-'`) |
| Global rules satisfied | **all 17** | `CLAUDE.md`; QA gauntlet (Phase 11) |
| Per-`.py` line cap | **0 offenders > 150 lines** | `scripts/check_line_cap.py` |
| Cost per run | **< `$5.00` budget cap** | Gatekeeper accumulated `total_cost_usd` |
| CI | **green on latest `main`** | GitHub Actions |
| Acceptance criteria | **A1–A15 each mapped to a passing test/artifact** | `docs/ACCEPTANCE.md` (Phase 11) |

## 7. Out of Scope (documented as extension points)

The following are explicitly **not** delivered in v1.00 but are designed-for and documented in `docs/PRD_extension_points.md` so they can be added without re-architecting:

- **Graphical UI (GUI).** Optional only; grading is on the terminal menu and SDK (A12). If a GUI is later added, it must be documented with screenshots and call the SDK exactly as the menu does.
- **Multi-topic tournaments / multi-round brackets.** v1.00 runs one topic, one debate (the configured `debate.topic`). New topics are config-only changes; tournament orchestration is a future extension.
- **Non-Claude LLM backends (e.g., GLM, Gemini, Codex).** v1.00 uses only `claude -p`. The runtime is interface-shaped so a new backend means implementing that interface — documented as an extension point, not built here.
- **Alternative judge rubrics / multi-judge panels.** v1.00 ships one persuasiveness rubric; swapping or adding rubrics is a documented extension.
- **Persistent per-agent LLM sessions (`claude --resume`).** Deliberately rejected in favor of stateless agents + orchestrator-owned context (rationale in `docs/PLAN.md` ADR-002); noted here so the choice is intentional, not an omission.

## 8. Assumptions, Constraints & Dependencies

**Assumptions**
- The grader and both authors have the **`claude` CLI installed and logged in on a Max (or Pro) subscription**; the headless path `claude -p --output-format json` works (smoke-tested in Phase 0). There is **no API key** anywhere.
- `WebSearch` is available to `claude -p` via `--allowedTools WebSearch`; a Python `WebSearchTool` (e.g., DuckDuckGo) is the documented fallback when a turn lacks citations (`docs/PRD_web_search.md`).
- The grader can run `uv` and Python 3.11 on a POSIX-like environment supporting `multiprocessing` with Queues.

**Constraints**
- **`uv` is the only package manager** (no pip / venv / `python script.py`); **150-line hard cap** per `.py`; **all business logic through the single `class SDK`**; **CLI-only development** (Claude Code in the terminal). All knobs are config-driven (`config/setup.json`, `config/gatekeeper.json`, `config/logging_config.json`) — **zero hardcoded** topic/pings/timeouts/budget/paths.
- **English-only** for all artifacts and debate output; **PC, respectful** debate language with enforced word limit (`max_words_per_turn = 180`).
- **Versioning starts at `1.00`** across `version.py`, every config `"version"`, and git tag `v1.00`. **Conventional Commits**, multiple per phase, both authors in `git shortlog -sn`.

**Dependencies**
- Runtime libs: `python-dotenv>=1.0`, `pydantic>=2.6` (protocol validation), `rich>=13.7` (menu rendering).
- Dev libs: `pytest>=8.0`, `pytest-cov>=4.1`, `pytest-mock>=3.12`, `ruff>=0.4`, `hypothesis>=6.100`, `pre-commit>=3.7`.
- External prerequisite (not pip-installed): the `claude` CLI.
- Ported HW1 modules: `shared/{config.py, version.py, logging_setup.py, gatekeeper.py}` (the Gatekeeper repurposed from an HTTP rate-limiter to a token/USD cost meter).

## 9. Timeline — Phase 0 → Phase 12

The build runs strictly top-to-bottom; each phase ends with updated `docs/TODO.md`, a saved prompt log (`docs/prompts/NNN_*.md`), Conventional Commits, a push to `main`, and a green CI run before the next phase begins.

| Phase | Title | Primary output | Key acceptance / KPI touched |
|---|---|---|---|
| **0** | Bootstrap + tooling + `CLAUDE.md` + CI (reuse HW1) | Scaffold, `config/*.json`, `pyproject.toml`, `uv.lock`, green CI | A14; rules 1–17 wired |
| **1** | Mandatory docs | This `PRD.md`, 12 per-mechanism PRDs, `PLAN.md` (C4 + sequence + ≥8 ADRs), `TODO.md` (≥600) | KPIs: ≥600 TODOs; A13 diagrams seeded |
| **2** | Shared infra: Config/version/logging (FIFO) + Gatekeeper (token economy) | `src/.../shared/`, `sdk/sdk.py` skeleton | A11 (Gatekeeper, FIFO, SDK), NFR-2/4/8 |
| **3** | Claude CLI runtime (`claude -p` JSON wrapper) | `src/.../runtime/` (`claude_cli.py`, `argv.py`, `parse.py`) | A7, A9 |
| **4** | Agent hierarchy + 3 distinct Skills | `src/.../agents/`, `src/.../skills/` | A2, A13, A10 |
| **5** | JSON IPC protocol (pydantic, routing) | `src/.../protocol/` (`message.py`, `routing.py`, `serialize.py`) | A5, A6 |
| **6** | Orchestrator + Watchdog (the working debate) | `src/.../orchestration/` (`process_agent.py`, `orchestrator.py`, `watchdog.py`, `loop.py`) | A1, A3, A4, A5, A9, A11 |
| **7** | Judge: enforce, score, no-tie verdict | `agents/judge.py`, `agents/verdict.py` | A4, A7, A8, A10 |
| **8** | Terminal menu + CLI | `src/.../cli/` (`menu.py`, `main.py`, `actions.py`) | A12 |
| **9** | Real debate run + transcript + diagrams + cost | `transcripts/session_001.json`, `assets/`, `docs/diagrams/`, cost report | A1, A3, A8, A13, A15; cost KPI |
| **10** | README lab report | `README.md` (≥250 lines, ≥5 images, full session-1 dialogue, cost, self-assessment) | A15 |
| **11** | QA gauntlet + acceptance audit | All gates green; `docs/ACCEPTANCE.md` mapping A1–A15 → test/artifact | all KPIs; all 17 rules |
| **12** | Cover PDF + tag + release + Moodle | `~/COSMOS77/HW2/COSMOS77-ex02.pdf` (exercise number = 2), git tag `v1.00`, GitHub Release | submission |

**Self-score recommendation:** **85**, set only if the Phase 11 gauntlet is genuinely green (rationale in `../CLAUDE_CODE_PLAYBOOK.md` §15 and the README Self-Assessment). 85 signals a senior-engineering bar met across every acceptance criterion while leaving honest room for review; we do not inflate to cover any unmet mandatory criterion.
