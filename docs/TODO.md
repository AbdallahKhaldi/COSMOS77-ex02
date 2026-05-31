# TODO — COSMOS77-ex02

Single source of truth for outstanding work. One task per line so
`grep -c '^T-' docs/TODO.md` counts them. Format:

```
  T-NNNN | <phase> | <area> | <description> | <definition-of-done> | <status>
```

Total tasks: 28 (P0) + the P1-P12 expansion below.
Statuses: P0 and P1 are done; P2-P12 are todo until their phase lands.

## Phase 0 — Repo bootstrap (done 2026-05-31)

T-0001 | P0 | repo | git init -b main, set user identity, add origin remote | remote shows ex02 URL; branch main | done 2026-05-31
T-0002 | P0 | repo | create directory layout (src package, tests, docs, config, logs, transcripts, assets) | tree matches playbook §2.2 task 1 | done 2026-05-31
T-0003 | P0 | repo | package skeleton: __init__.py with module docstrings for every subpackage | import cosmos77_ex02 succeeds | done 2026-05-31
T-0004 | P0 | build | pyproject.toml: name, version 1.00, deps, dev group, script, ruff/coverage/pytest config | uv sync resolves | done 2026-05-31
T-0005 | P0 | build | .python-version = 3.11 | file present | done 2026-05-31
T-0006 | P0 | repo | .gitignore: env, caches, logs, transcripts, pdf; keep .gitkeep + session_001 | status ignores .venv/.env | done 2026-05-31
T-0007 | P0 | cyber | .env.example placeholders only (claude CLI login; no keys) | no real secrets; .env gitignored | done 2026-05-31
T-0008 | P0 | config | config/setup.json (debate/runtime/orchestration/paths) | valid JSON; version 1.00 | done 2026-05-31
T-0009 | P0 | config | config/gatekeeper.json (budget cap 5.00) | valid JSON; version 1.00 | done 2026-05-31
T-0010 | P0 | config | config/logging_config.json (FIFO 20x500 handler reference) | valid JSON; dictConfig version 1 | done 2026-05-31
T-0011 | P0 | governance | CLAUDE.md (17 rules verbatim from playbook §17) | matches Appendix A | done 2026-05-31
T-0012 | P0 | docs | README.md placeholder (full report in Phase 10) | renders; links resolve | done 2026-05-31
T-0013 | P0 | governance | LICENSE (MIT, 2026, both authors) | present | done 2026-05-31
T-0014 | P0 | governance | CHANGELOG.md Keep-a-Changelog [1.00] entry | present | done 2026-05-31
T-0015 | P0 | governance | CONTRIBUTING.md (rules, commits, gates, prompt-log) | present | done 2026-05-31
T-0016 | P0 | governance | BADGES.md (ex02 CI badge + python/license/uv/coverage) | present | done 2026-05-31
T-0017 | P0 | quality | scripts/check_line_cap.py (<=150 enforcement) | 0 offenders | done 2026-05-31
T-0018 | P0 | quality | scripts/generate_cover_pdf.py (ported; retargeted in Phase 12) | imports parse; lints clean | done 2026-05-31
T-0019 | P0 | quality | .pre-commit-config.yaml (ruff + std hooks + local line-cap) | pre-commit wiring valid | done 2026-05-31
T-0020 | P0 | ci | .github/workflows/ci.yml (uv sync --frozen, ruff, line-cap, pytest cov gate, exclude live) | workflow valid YAML | done 2026-05-31
T-0021 | P0 | core | constants.py (ROLES, TURN_TYPES, DEFAULT_ENCODING) | importable; <=30 lines | done 2026-05-31
T-0022 | P0 | test | tests/unit/test_constants.py + conftest.py harness | pytest collects >=1 test; constants 100% | done 2026-05-31
T-0023 | P0 | docs | docs PRD/PLAN placeholders (14 stubs) for Phase 1 | files present with per-file scope | done 2026-05-31
T-0024 | P0 | build | uv sync -> .venv + uv.lock committed | both exist; uv lock --check passes | done 2026-05-31
T-0025 | P0 | quality | ruff check zero + ruff format clean + line-cap 0 + pytest >=85% | all gates green locally | done 2026-05-31
T-0026 | P0 | quality | pre-commit installed in the local repo | .git/hooks/pre-commit present | done 2026-05-31
T-0027 | P0 | docs | docs/prompts/000_phase0_bootstrap.md (prompt + summary) | present | done 2026-05-31
T-0028 | P0 | ci | conventional commits (both authors) + push origin main + CI green | Actions green on main | done 2026-05-31

## Phase 1 — Mandatory docs

T-0029 | P1 | prd | PRD: context & rationale (Prompt vs Context Engineering, why 3-agent debate) | section present and substantive | done 2026-05-31
T-0030 | P1 | prd | PRD: stakeholders (grader, two partners, lecturer) | section present and substantive | done 2026-05-31
T-0031 | P1 | prd | PRD: user stories (run one command; watch judged debate) | section present and substantive | done 2026-05-31
T-0032 | P1 | prd | PRD: functional requirements table mapped to A1-A15 | section present and substantive | done 2026-05-31
T-0033 | P1 | prd | PRD: non-functional requirements (robustness, cost, reproducibility, testability, English) | section present and substantive | done 2026-05-31
T-0034 | P1 | prd | PRD: KPIs (>=10 pings, 0 ties, >=1 citation/turn, >=85% cov, 0 ruff, >=600 TODO) | section present and substantive | done 2026-05-31
T-0035 | P1 | prd | PRD: out-of-scope (GUI, tournaments, non-Claude backends) | section present and substantive | done 2026-05-31
T-0036 | P1 | prd | PRD: assumptions/constraints/dependencies (claude CLI, English, PC) | section present and substantive | done 2026-05-31
T-0037 | P1 | prd | PRD: timeline Phase 0 -> Phase 12 table | section present and substantive | done 2026-05-31
T-0038 | P1 | prd | write docs/PRD_agent_base.md (responsibilities, lifecycle, errors, acceptance map) | doc complete and cross-linked | done 2026-05-31
T-0039 | P1 | prd | review docs/PRD_agent_base.md against acceptance criteria and config values | values match config; A-ids cited | done 2026-05-31
T-0040 | P1 | prd | write docs/PRD_judge_agent.md (responsibilities, lifecycle, errors, acceptance map) | doc complete and cross-linked | done 2026-05-31
T-0041 | P1 | prd | review docs/PRD_judge_agent.md against acceptance criteria and config values | values match config; A-ids cited | done 2026-05-31
T-0042 | P1 | prd | write docs/PRD_debater_agents.md (responsibilities, lifecycle, errors, acceptance map) | doc complete and cross-linked | done 2026-05-31
T-0043 | P1 | prd | review docs/PRD_debater_agents.md against acceptance criteria and config values | values match config; A-ids cited | done 2026-05-31
T-0044 | P1 | prd | write docs/PRD_skills.md (responsibilities, lifecycle, errors, acceptance map) | doc complete and cross-linked | done 2026-05-31
T-0045 | P1 | prd | review docs/PRD_skills.md against acceptance criteria and config values | values match config; A-ids cited | done 2026-05-31
T-0046 | P1 | prd | write docs/PRD_ipc_protocol.md (responsibilities, lifecycle, errors, acceptance map) | doc complete and cross-linked | done 2026-05-31
T-0047 | P1 | prd | review docs/PRD_ipc_protocol.md against acceptance criteria and config values | values match config; A-ids cited | done 2026-05-31
T-0048 | P1 | prd | write docs/PRD_orchestrator.md (responsibilities, lifecycle, errors, acceptance map) | doc complete and cross-linked | done 2026-05-31
T-0049 | P1 | prd | review docs/PRD_orchestrator.md against acceptance criteria and config values | values match config; A-ids cited | done 2026-05-31
T-0050 | P1 | prd | write docs/PRD_watchdog.md (responsibilities, lifecycle, errors, acceptance map) | doc complete and cross-linked | done 2026-05-31
T-0051 | P1 | prd | review docs/PRD_watchdog.md against acceptance criteria and config values | values match config; A-ids cited | done 2026-05-31
T-0052 | P1 | prd | write docs/PRD_gatekeeper.md (responsibilities, lifecycle, errors, acceptance map) | doc complete and cross-linked | done 2026-05-31
T-0053 | P1 | prd | review docs/PRD_gatekeeper.md against acceptance criteria and config values | values match config; A-ids cited | done 2026-05-31
T-0054 | P1 | prd | write docs/PRD_logging.md (responsibilities, lifecycle, errors, acceptance map) | doc complete and cross-linked | done 2026-05-31
T-0055 | P1 | prd | review docs/PRD_logging.md against acceptance criteria and config values | values match config; A-ids cited | done 2026-05-31
T-0056 | P1 | prd | write docs/PRD_web_search.md (responsibilities, lifecycle, errors, acceptance map) | doc complete and cross-linked | done 2026-05-31
T-0057 | P1 | prd | review docs/PRD_web_search.md against acceptance criteria and config values | values match config; A-ids cited | done 2026-05-31
T-0058 | P1 | prd | write docs/PRD_terminal_menu.md (responsibilities, lifecycle, errors, acceptance map) | doc complete and cross-linked | done 2026-05-31
T-0059 | P1 | prd | review docs/PRD_terminal_menu.md against acceptance criteria and config values | values match config; A-ids cited | done 2026-05-31
T-0060 | P1 | prd | write docs/PRD_extension_points.md (responsibilities, lifecycle, errors, acceptance map) | doc complete and cross-linked | done 2026-05-31
T-0061 | P1 | prd | review docs/PRD_extension_points.md against acceptance criteria and config values | values match config; A-ids cited | done 2026-05-31
T-0062 | P1 | plan | PLAN: C4 Context diagram (mermaid) | section present in PLAN.md | done 2026-05-31
T-0063 | P1 | plan | PLAN: C4 Container diagram (mermaid) | section present in PLAN.md | done 2026-05-31
T-0064 | P1 | plan | PLAN: C4 Component diagram (mermaid) | section present in PLAN.md | done 2026-05-31
T-0065 | P1 | plan | PLAN: Code-level classDiagram (mermaid) | section present in PLAN.md | done 2026-05-31
T-0066 | P1 | plan | PLAN: sequenceDiagram of one full ping (mermaid) | section present in PLAN.md | done 2026-05-31
T-0067 | P1 | plan | PLAN: ADR-001 Claude CLI headless over Agent SDK/API key | section present in PLAN.md | done 2026-05-31
T-0068 | P1 | plan | PLAN: ADR-002 stateless agents + orchestrator-owned context | section present in PLAN.md | done 2026-05-31
T-0069 | P1 | plan | PLAN: ADR-003 multiprocessing + Queues for IPC | section present in PLAN.md | done 2026-05-31
T-0070 | P1 | plan | PLAN: ADR-004 JSON + pydantic protocol | section present in PLAN.md | done 2026-05-31
T-0071 | P1 | plan | PLAN: ADR-005 SDK single entry point | section present in PLAN.md | done 2026-05-31
T-0072 | P1 | plan | PLAN: ADR-006 uv-only | section present in PLAN.md | done 2026-05-31
T-0073 | P1 | plan | PLAN: ADR-007 150-line cap | section present in PLAN.md | done 2026-05-31
T-0074 | P1 | plan | PLAN: ADR-008 Gatekeeper budget cap value/rationale | section present in PLAN.md | done 2026-05-31
T-0075 | P1 | plan | PLAN: phased roadmap mirroring the playbook | section present in PLAN.md | done 2026-05-31
T-0076 | P1 | plan | PLAN: risk register (stalls, citation-less turns, auto-agree, budget overrun) | section present in PLAN.md | done 2026-05-31
T-0077 | P1 | docs | expand docs/TODO.md to >=600 granular tasks | Phase 1 verification block passes | done 2026-05-31
T-0078 | P1 | docs | save docs/prompts/001_phase1_docs.md (prompt + summary) | Phase 1 verification block passes | done 2026-05-31
T-0079 | P1 | docs | cross-link all docs and verify references resolve | Phase 1 verification block passes | done 2026-05-31
T-0080 | P1 | docs | verify grep counts (TODO >=600, PRD_*.md >=12, ADR- >=8, diagrams >=1 each) | Phase 1 verification block passes | done 2026-05-31
T-0081 | P1 | docs | commit docs in batches and push; confirm CI green | Phase 1 verification block passes | done 2026-05-31

## Phase 2 — Shared infrastructure

T-0082 | P2 | shared | design shared/version.py public interface and signatures | interface documented in PRD/PLAN; reviewed | done 2026-05-31
T-0083 | P2 | shared | test(shared): happy-path for VERSION=1.00 + validate_config_version | failing test written first (red) | done 2026-05-31
T-0084 | P2 | shared | test(shared): error-path for VERSION=1.00 + validate_config_version | raises/handles the error path; test green | done 2026-05-31
T-0085 | P2 | shared | test(shared): edge-case/property test for shared/version.py | boundary inputs covered | done 2026-05-31
T-0086 | P2 | shared | implement shared/version.py: VERSION=1.00 + validate_config_version | smallest impl that passes tests (green) | done 2026-05-31
T-0087 | P2 | shared | docstrings on shared/version.py public API (why, not what) | every public symbol documented | done 2026-05-31
T-0088 | P2 | shared | type hints on shared/version.py public signatures (no bare Any) | mypy-clean signatures | done 2026-05-31
T-0089 | P2 | shared | review shared/version.py for duplication (rule 3) | no copy-paste; shared helpers extracted | done 2026-05-31
T-0090 | P2 | shared | keep shared/version.py <=150 lines; split helpers if needed | check_line_cap 0 offenders | done 2026-05-31
T-0091 | P2 | shared | integrate shared/version.py with the SDK / its callers | SDK method or caller wired and tested | done 2026-05-31
T-0092 | P2 | shared | design shared/config.py public interface and signatures | interface documented in PRD/PLAN; reviewed | done 2026-05-31
T-0093 | P2 | shared | test(shared): happy-path for Config loader dot-path access + .env + version validation | failing test written first (red) | done 2026-05-31
T-0094 | P2 | shared | test(shared): error-path for Config loader dot-path access + .env + version validation | raises/handles the error path; test green | done 2026-05-31
T-0095 | P2 | shared | test(shared): edge-case/property test for shared/config.py | boundary inputs covered | done 2026-05-31
T-0096 | P2 | shared | implement shared/config.py: Config loader dot-path access + .env + version validation | smallest impl that passes tests (green) | done 2026-05-31
T-0097 | P2 | shared | docstrings on shared/config.py public API (why, not what) | every public symbol documented | done 2026-05-31
T-0098 | P2 | shared | type hints on shared/config.py public signatures (no bare Any) | mypy-clean signatures | done 2026-05-31
T-0099 | P2 | shared | review shared/config.py for duplication (rule 3) | no copy-paste; shared helpers extracted | done 2026-05-31
T-0100 | P2 | shared | keep shared/config.py <=150 lines; split helpers if needed | check_line_cap 0 offenders | done 2026-05-31
T-0101 | P2 | shared | integrate shared/config.py with the SDK / its callers | SDK method or caller wired and tested | done 2026-05-31
T-0102 | P2 | shared | design shared/logging_setup.py public interface and signatures | interface documented in PRD/PLAN; reviewed | done 2026-05-31
T-0103 | P2 | shared | test(shared): happy-path for initialize logging from logging_config.json | failing test written first (red) | done 2026-05-31
T-0104 | P2 | shared | test(shared): error-path for initialize logging from logging_config.json | raises/handles the error path; test green | done 2026-05-31
T-0105 | P2 | shared | test(shared): edge-case/property test for shared/logging_setup.py | boundary inputs covered | done 2026-05-31
T-0106 | P2 | shared | implement shared/logging_setup.py: initialize logging from logging_config.json | smallest impl that passes tests (green) | done 2026-05-31
T-0107 | P2 | shared | docstrings on shared/logging_setup.py public API (why, not what) | every public symbol documented | done 2026-05-31
T-0108 | P2 | shared | type hints on shared/logging_setup.py public signatures (no bare Any) | mypy-clean signatures | done 2026-05-31
T-0109 | P2 | shared | review shared/logging_setup.py for duplication (rule 3) | no copy-paste; shared helpers extracted | done 2026-05-31
T-0110 | P2 | shared | keep shared/logging_setup.py <=150 lines; split helpers if needed | check_line_cap 0 offenders | done 2026-05-31
T-0111 | P2 | shared | integrate shared/logging_setup.py with the SDK / its callers | SDK method or caller wired and tested | done 2026-05-31
T-0112 | P2 | shared | design shared/fifo_handler.py public interface and signatures | interface documented in PRD/PLAN; reviewed | done 2026-05-31
T-0113 | P2 | shared | test(shared): happy-path for FifoLineRotatingHandler 20 files x 500 lines | failing test written first (red) | done 2026-05-31
T-0114 | P2 | shared | test(shared): error-path for FifoLineRotatingHandler 20 files x 500 lines | raises/handles the error path; test green | done 2026-05-31
T-0115 | P2 | shared | test(shared): edge-case/property test for shared/fifo_handler.py | boundary inputs covered | done 2026-05-31
T-0116 | P2 | shared | implement shared/fifo_handler.py: FifoLineRotatingHandler 20 files x 500 lines | smallest impl that passes tests (green) | done 2026-05-31
T-0117 | P2 | shared | docstrings on shared/fifo_handler.py public API (why, not what) | every public symbol documented | done 2026-05-31
T-0118 | P2 | shared | type hints on shared/fifo_handler.py public signatures (no bare Any) | mypy-clean signatures | done 2026-05-31
T-0119 | P2 | shared | review shared/fifo_handler.py for duplication (rule 3) | no copy-paste; shared helpers extracted | done 2026-05-31
T-0120 | P2 | shared | keep shared/fifo_handler.py <=150 lines; split helpers if needed | check_line_cap 0 offenders | done 2026-05-31
T-0121 | P2 | shared | integrate shared/fifo_handler.py with the SDK / its callers | SDK method or caller wired and tested | done 2026-05-31
T-0122 | P2 | shared | design shared/gatekeeper.py public interface and signatures | interface documented in PRD/PLAN; reviewed | done 2026-05-31
T-0123 | P2 | shared | test(shared): happy-path for cost meter: account/check_budget/guard/scrub + BudgetExceeded | failing test written first (red) | done 2026-05-31
T-0124 | P2 | shared | test(shared): error-path for cost meter: account/check_budget/guard/scrub + BudgetExceeded | raises/handles the error path; test green | done 2026-05-31
T-0125 | P2 | shared | test(shared): edge-case/property test for shared/gatekeeper.py | boundary inputs covered | done 2026-05-31
T-0126 | P2 | shared | implement shared/gatekeeper.py: cost meter: account/check_budget/guard/scrub + BudgetExceeded | smallest impl that passes tests (green) | done 2026-05-31
T-0127 | P2 | shared | docstrings on shared/gatekeeper.py public API (why, not what) | every public symbol documented | done 2026-05-31
T-0128 | P2 | shared | type hints on shared/gatekeeper.py public signatures (no bare Any) | mypy-clean signatures | done 2026-05-31
T-0129 | P2 | shared | review shared/gatekeeper.py for duplication (rule 3) | no copy-paste; shared helpers extracted | done 2026-05-31
T-0130 | P2 | shared | keep shared/gatekeeper.py <=150 lines; split helpers if needed | check_line_cap 0 offenders | done 2026-05-31
T-0131 | P2 | shared | integrate shared/gatekeeper.py with the SDK / its callers | SDK method or caller wired and tested | done 2026-05-31
T-0132 | P2 | shared | design shared/errors.py public interface and signatures | interface documented in PRD/PLAN; reviewed | done 2026-05-31
T-0133 | P2 | shared | test(shared): happy-path for shared exception types (BudgetExceeded, RuntimeTimeout, ConfigError) | failing test written first (red) | done 2026-05-31
T-0134 | P2 | shared | test(shared): error-path for shared exception types (BudgetExceeded, RuntimeTimeout, ConfigError) | raises/handles the error path; test green | done 2026-05-31
T-0135 | P2 | shared | test(shared): edge-case/property test for shared/errors.py | boundary inputs covered | done 2026-05-31
T-0136 | P2 | shared | implement shared/errors.py: shared exception types (BudgetExceeded, RuntimeTimeout, ConfigError) | smallest impl that passes tests (green) | done 2026-05-31
T-0137 | P2 | shared | docstrings on shared/errors.py public API (why, not what) | every public symbol documented | done 2026-05-31
T-0138 | P2 | shared | type hints on shared/errors.py public signatures (no bare Any) | mypy-clean signatures | done 2026-05-31
T-0139 | P2 | shared | review shared/errors.py for duplication (rule 3) | no copy-paste; shared helpers extracted | done 2026-05-31
T-0140 | P2 | shared | keep shared/errors.py <=150 lines; split helpers if needed | check_line_cap 0 offenders | done 2026-05-31
T-0141 | P2 | shared | integrate shared/errors.py with the SDK / its callers | SDK method or caller wired and tested | done 2026-05-31
T-0142 | P2 | shared | design sdk/sdk.py public interface and signatures | interface documented in PRD/PLAN; reviewed | done 2026-05-31
T-0143 | P2 | shared | test(shared): happy-path for SDK skeleton with stubbed public methods | failing test written first (red) | done 2026-05-31
T-0144 | P2 | shared | test(shared): error-path for SDK skeleton with stubbed public methods | raises/handles the error path; test green | done 2026-05-31
T-0145 | P2 | shared | test(shared): edge-case/property test for sdk/sdk.py | boundary inputs covered | done 2026-05-31
T-0146 | P2 | shared | implement sdk/sdk.py: SDK skeleton with stubbed public methods | smallest impl that passes tests (green) | done 2026-05-31
T-0147 | P2 | shared | docstrings on sdk/sdk.py public API (why, not what) | every public symbol documented | done 2026-05-31
T-0148 | P2 | shared | type hints on sdk/sdk.py public signatures (no bare Any) | mypy-clean signatures | done 2026-05-31
T-0149 | P2 | shared | review sdk/sdk.py for duplication (rule 3) | no copy-paste; shared helpers extracted | done 2026-05-31
T-0150 | P2 | shared | keep sdk/sdk.py <=150 lines; split helpers if needed | check_line_cap 0 offenders | done 2026-05-31
T-0151 | P2 | shared | integrate sdk/sdk.py with the SDK / its callers | SDK method or caller wired and tested | done 2026-05-31
T-0152 | P2 | shared | Config: dot-path access cfg.get('debate.pings_per_side') | task complete and tested | done 2026-05-31
T-0153 | P2 | shared | Config: missing-key returns default; missing-file raises clear error | task complete and tested | done 2026-05-31
T-0154 | P2 | shared | Config: load .env via python-dotenv | task complete and tested | done 2026-05-31
T-0155 | P2 | shared | version: validate_config_version mismatch raises | task complete and tested | done 2026-05-31
T-0156 | P2 | shared | gatekeeper: accrue cost from a fake claude -p JSON result | task complete and tested | done 2026-05-31
T-0157 | P2 | shared | gatekeeper: raise BudgetExceeded at budget_usd_max | task complete and tested | done 2026-05-31
T-0158 | P2 | shared | gatekeeper: warn at warn_at_fraction (0.8) | task complete and tested | done 2026-05-31
T-0159 | P2 | shared | gatekeeper: per_call_usd_max enforcement | task complete and tested | done 2026-05-31
T-0160 | P2 | shared | gatekeeper: scrub() redacts a fake key/token | task complete and tested | done 2026-05-31
T-0161 | P2 | shared | fifo: rotate at 500 lines; keep newest 20 files; drop oldest | task complete and tested | done 2026-05-31
T-0162 | P2 | shared | fifo: JSON-lines event format | task complete and tested | done 2026-05-31
T-0163 | P2 | shared | constants: confirm ROLES/TURN_TYPES from Phase 0 | task complete and tested | done 2026-05-31
T-0164 | P2 | shared | SDK: run_debate/set_topic/last_verdict/cost_report/tail_logs raise NotImplementedError | task complete and tested | done 2026-05-31
T-0165 | P2 | shared | tests under tests/unit/test_shared/ pass; coverage >=85% | task complete and tested | done 2026-05-31
T-0166 | P2 | shared | update TODO; save docs/prompts/002; commit per module; push; CI green | task complete and tested | done 2026-05-31

## Phase 3 — Claude CLI runtime

T-0167 | P3 | runtime | design runtime/argv.py public interface and signatures | interface documented in PRD/PLAN; reviewed | done 2026-05-31
T-0168 | P3 | runtime | test(runtime): happy-path for build claude -p argv (--output-format json, --append-system-prompt, --allowedTools, timeout) | failing test written first (red) | done 2026-05-31
T-0169 | P3 | runtime | test(runtime): error-path for build claude -p argv (--output-format json, --append-system-prompt, --allowedTools, timeout) | raises/handles the error path; test green | done 2026-05-31
T-0170 | P3 | runtime | test(runtime): edge-case/property test for runtime/argv.py | boundary inputs covered | done 2026-05-31
T-0171 | P3 | runtime | implement runtime/argv.py: build claude -p argv (--output-format json, --append-system-prompt, --allowedTools, timeout) | smallest impl that passes tests (green) | done 2026-05-31
T-0172 | P3 | runtime | docstrings on runtime/argv.py public API (why, not what) | every public symbol documented | done 2026-05-31
T-0173 | P3 | runtime | type hints on runtime/argv.py public signatures (no bare Any) | mypy-clean signatures | done 2026-05-31
T-0174 | P3 | runtime | review runtime/argv.py for duplication (rule 3) | no copy-paste; shared helpers extracted | done 2026-05-31
T-0175 | P3 | runtime | keep runtime/argv.py <=150 lines; split helpers if needed | check_line_cap 0 offenders | done 2026-05-31
T-0176 | P3 | runtime | integrate runtime/argv.py with the SDK / its callers | SDK method or caller wired and tested | done 2026-05-31
T-0177 | P3 | runtime | design runtime/parse.py public interface and signatures | interface documented in PRD/PLAN; reviewed | done 2026-05-31
T-0178 | P3 | runtime | test(runtime): happy-path for parse claude -p JSON into LlmResult | failing test written first (red) | done 2026-05-31
T-0179 | P3 | runtime | test(runtime): error-path for parse claude -p JSON into LlmResult | raises/handles the error path; test green | done 2026-05-31
T-0180 | P3 | runtime | test(runtime): edge-case/property test for runtime/parse.py | boundary inputs covered | done 2026-05-31
T-0181 | P3 | runtime | implement runtime/parse.py: parse claude -p JSON into LlmResult | smallest impl that passes tests (green) | done 2026-05-31
T-0182 | P3 | runtime | docstrings on runtime/parse.py public API (why, not what) | every public symbol documented | done 2026-05-31
T-0183 | P3 | runtime | type hints on runtime/parse.py public signatures (no bare Any) | mypy-clean signatures | done 2026-05-31
T-0184 | P3 | runtime | review runtime/parse.py for duplication (rule 3) | no copy-paste; shared helpers extracted | done 2026-05-31
T-0185 | P3 | runtime | keep runtime/parse.py <=150 lines; split helpers if needed | check_line_cap 0 offenders | done 2026-05-31
T-0186 | P3 | runtime | integrate runtime/parse.py with the SDK / its callers | SDK method or caller wired and tested | done 2026-05-31
T-0187 | P3 | runtime | design runtime/claude_cli.py public interface and signatures | interface documented in PRD/PLAN; reviewed | done 2026-05-31
T-0188 | P3 | runtime | test(runtime): happy-path for ClaudeCliRuntime.invoke via subprocess.run with timeout | failing test written first (red) | done 2026-05-31
T-0189 | P3 | runtime | test(runtime): error-path for ClaudeCliRuntime.invoke via subprocess.run with timeout | raises/handles the error path; test green | done 2026-05-31
T-0190 | P3 | runtime | test(runtime): edge-case/property test for runtime/claude_cli.py | boundary inputs covered | done 2026-05-31
T-0191 | P3 | runtime | implement runtime/claude_cli.py: ClaudeCliRuntime.invoke via subprocess.run with timeout | smallest impl that passes tests (green) | done 2026-05-31
T-0192 | P3 | runtime | docstrings on runtime/claude_cli.py public API (why, not what) | every public symbol documented | done 2026-05-31
T-0193 | P3 | runtime | type hints on runtime/claude_cli.py public signatures (no bare Any) | mypy-clean signatures | done 2026-05-31
T-0194 | P3 | runtime | review runtime/claude_cli.py for duplication (rule 3) | no copy-paste; shared helpers extracted | done 2026-05-31
T-0195 | P3 | runtime | keep runtime/claude_cli.py <=150 lines; split helpers if needed | check_line_cap 0 offenders | done 2026-05-31
T-0196 | P3 | runtime | integrate runtime/claude_cli.py with the SDK / its callers | SDK method or caller wired and tested | done 2026-05-31
T-0197 | P3 | runtime | LlmResult dataclass: text, cost_usd, input_tokens, output_tokens, session_id, is_error, raw | task complete and tested | done 2026-05-31
T-0198 | P3 | runtime | build correct argv from Config defaults | task complete and tested | done 2026-05-31
T-0199 | P3 | runtime | parse result text + total_cost_usd + usage + session_id | task complete and tested | done 2026-05-31
T-0200 | P3 | runtime | raise RuntimeTimeout when subprocess exceeds per_call_timeout_seconds | task complete and tested | done 2026-05-31
T-0201 | P3 | runtime | raise RuntimeError on is_error or non-zero exit | task complete and tested | done 2026-05-31
T-0202 | P3 | runtime | malformed JSON -> informative error | task complete and tested | done 2026-05-31
T-0203 | P3 | runtime | missing cost field -> default 0 + warning | task complete and tested | done 2026-05-31
T-0204 | P3 | runtime | mock subprocess in ALL tests (never call real claude) | task complete and tested | done 2026-05-31
T-0205 | P3 | runtime | verify no live LLM call in the suite (marker live excluded) | task complete and tested | done 2026-05-31
T-0206 | P3 | runtime | coverage >=90% on runtime/ | task complete and tested | done 2026-05-31
T-0207 | P3 | runtime | update TODO; save docs/prompts/003; commit (>=3); push; CI green | task complete and tested | done 2026-05-31

## Phase 4 — Agent hierarchy + Skills

T-0208 | P4 | skills | skill_pro.md: evidence-driven optimist persona + Description selector line | skill files present and distinct | done 2026-05-31
T-0209 | P4 | skills | skill_con.md: critical skeptic persona, distinct argumentative strategy | skill files present and distinct | done 2026-05-31
T-0210 | P4 | skills | skill_judge.md: rules-only rubric; scores persuasion; no right answer; forbids ties | skill files present and distinct | done 2026-05-31
T-0211 | P4 | skills | assert three skills exist, non-empty, with distinct Description lines | skill files present and distinct | done 2026-05-31
T-0212 | P4 | skills | skills are English and PC | skill files present and distinct | done 2026-05-31
T-0213 | P4 | agents | design agents/base.py public interface and signatures | interface documented in PRD/PLAN; reviewed | done 2026-05-31
T-0214 | P4 | agents | test(agents): happy-path for BaseAgent(ABC): role, skill, runtime, gatekeeper; act() abstract; shared helpers | failing test written first (red) | done 2026-05-31
T-0215 | P4 | agents | test(agents): error-path for BaseAgent(ABC): role, skill, runtime, gatekeeper; act() abstract; shared helpers | raises/handles the error path; test green | done 2026-05-31
T-0216 | P4 | agents | test(agents): edge-case/property test for agents/base.py | boundary inputs covered | done 2026-05-31
T-0217 | P4 | agents | implement agents/base.py: BaseAgent(ABC): role, skill, runtime, gatekeeper; act() abstract; shared helpers | smallest impl that passes tests (green) | done 2026-05-31
T-0218 | P4 | agents | docstrings on agents/base.py public API (why, not what) | every public symbol documented | done 2026-05-31
T-0219 | P4 | agents | type hints on agents/base.py public signatures (no bare Any) | mypy-clean signatures | done 2026-05-31
T-0220 | P4 | agents | review agents/base.py for duplication (rule 3) | no copy-paste; shared helpers extracted | done 2026-05-31
T-0221 | P4 | agents | keep agents/base.py <=150 lines; split helpers if needed | check_line_cap 0 offenders | done 2026-05-31
T-0222 | P4 | agents | integrate agents/base.py with the SDK / its callers | SDK method or caller wired and tested | done 2026-05-31
T-0223 | P4 | agents | design agents/debater.py public interface and signatures | interface documented in PRD/PLAN; reviewed | done 2026-05-31
T-0224 | P4 | agents | test(agents): happy-path for DebaterAgent.act(): rebut + new point + citation + word limit | failing test written first (red) | done 2026-05-31
T-0225 | P4 | agents | test(agents): error-path for DebaterAgent.act(): rebut + new point + citation + word limit | raises/handles the error path; test green | done 2026-05-31
T-0226 | P4 | agents | test(agents): edge-case/property test for agents/debater.py | boundary inputs covered | done 2026-05-31
T-0227 | P4 | agents | implement agents/debater.py: DebaterAgent.act(): rebut + new point + citation + word limit | smallest impl that passes tests (green) | done 2026-05-31
T-0228 | P4 | agents | docstrings on agents/debater.py public API (why, not what) | every public symbol documented | done 2026-05-31
T-0229 | P4 | agents | type hints on agents/debater.py public signatures (no bare Any) | mypy-clean signatures | done 2026-05-31
T-0230 | P4 | agents | review agents/debater.py for duplication (rule 3) | no copy-paste; shared helpers extracted | done 2026-05-31
T-0231 | P4 | agents | keep agents/debater.py <=150 lines; split helpers if needed | check_line_cap 0 offenders | done 2026-05-31
T-0232 | P4 | agents | integrate agents/debater.py with the SDK / its callers | SDK method or caller wired and tested | done 2026-05-31
T-0233 | P4 | agents | design agents/pro.py public interface and signatures | interface documented in PRD/PLAN; reviewed | done 2026-05-31
T-0234 | P4 | agents | test(agents): happy-path for ProAgent(DebaterAgent): loads skill_pro, fixed Pro position | failing test written first (red) | done 2026-05-31
T-0235 | P4 | agents | test(agents): error-path for ProAgent(DebaterAgent): loads skill_pro, fixed Pro position | raises/handles the error path; test green | done 2026-05-31
T-0236 | P4 | agents | test(agents): edge-case/property test for agents/pro.py | boundary inputs covered | done 2026-05-31
T-0237 | P4 | agents | implement agents/pro.py: ProAgent(DebaterAgent): loads skill_pro, fixed Pro position | smallest impl that passes tests (green) | done 2026-05-31
T-0238 | P4 | agents | docstrings on agents/pro.py public API (why, not what) | every public symbol documented | done 2026-05-31
T-0239 | P4 | agents | type hints on agents/pro.py public signatures (no bare Any) | mypy-clean signatures | done 2026-05-31
T-0240 | P4 | agents | review agents/pro.py for duplication (rule 3) | no copy-paste; shared helpers extracted | done 2026-05-31
T-0241 | P4 | agents | keep agents/pro.py <=150 lines; split helpers if needed | check_line_cap 0 offenders | done 2026-05-31
T-0242 | P4 | agents | integrate agents/pro.py with the SDK / its callers | SDK method or caller wired and tested | done 2026-05-31
T-0243 | P4 | agents | design agents/con.py public interface and signatures | interface documented in PRD/PLAN; reviewed | done 2026-05-31
T-0244 | P4 | agents | test(agents): happy-path for ConAgent(DebaterAgent): loads skill_con, fixed Con position | failing test written first (red) | done 2026-05-31
T-0245 | P4 | agents | test(agents): error-path for ConAgent(DebaterAgent): loads skill_con, fixed Con position | raises/handles the error path; test green | done 2026-05-31
T-0246 | P4 | agents | test(agents): edge-case/property test for agents/con.py | boundary inputs covered | done 2026-05-31
T-0247 | P4 | agents | implement agents/con.py: ConAgent(DebaterAgent): loads skill_con, fixed Con position | smallest impl that passes tests (green) | done 2026-05-31
T-0248 | P4 | agents | docstrings on agents/con.py public API (why, not what) | every public symbol documented | done 2026-05-31
T-0249 | P4 | agents | type hints on agents/con.py public signatures (no bare Any) | mypy-clean signatures | done 2026-05-31
T-0250 | P4 | agents | review agents/con.py for duplication (rule 3) | no copy-paste; shared helpers extracted | done 2026-05-31
T-0251 | P4 | agents | keep agents/con.py <=150 lines; split helpers if needed | check_line_cap 0 offenders | done 2026-05-31
T-0252 | P4 | agents | integrate agents/con.py with the SDK / its callers | SDK method or caller wired and tested | done 2026-05-31
T-0253 | P4 | agents | design agents/judge.py public interface and signatures | interface documented in PRD/PLAN; reviewed | done 2026-05-31
T-0254 | P4 | agents | test(agents): happy-path for JudgeAgent: relay/enforce/score_turn/verdict | failing test written first (red) | done 2026-05-31
T-0255 | P4 | agents | test(agents): error-path for JudgeAgent: relay/enforce/score_turn/verdict | raises/handles the error path; test green | done 2026-05-31
T-0256 | P4 | agents | test(agents): edge-case/property test for agents/judge.py | boundary inputs covered | done 2026-05-31
T-0257 | P4 | agents | implement agents/judge.py: JudgeAgent: relay/enforce/score_turn/verdict | smallest impl that passes tests (green) | done 2026-05-31
T-0258 | P4 | agents | docstrings on agents/judge.py public API (why, not what) | every public symbol documented | done 2026-05-31
T-0259 | P4 | agents | type hints on agents/judge.py public signatures (no bare Any) | mypy-clean signatures | done 2026-05-31
T-0260 | P4 | agents | review agents/judge.py for duplication (rule 3) | no copy-paste; shared helpers extracted | done 2026-05-31
T-0261 | P4 | agents | keep agents/judge.py <=150 lines; split helpers if needed | check_line_cap 0 offenders | done 2026-05-31
T-0262 | P4 | agents | integrate agents/judge.py with the SDK / its callers | SDK method or caller wired and tested | done 2026-05-31
T-0263 | P4 | agents | design agents/factory.py public interface and signatures | interface documented in PRD/PLAN; reviewed | done 2026-05-31
T-0264 | P4 | agents | test(agents): happy-path for build_agent(role, cfg); unknown role raises | failing test written first (red) | done 2026-05-31
T-0265 | P4 | agents | test(agents): error-path for build_agent(role, cfg); unknown role raises | raises/handles the error path; test green | done 2026-05-31
T-0266 | P4 | agents | test(agents): edge-case/property test for agents/factory.py | boundary inputs covered | done 2026-05-31
T-0267 | P4 | agents | implement agents/factory.py: build_agent(role, cfg); unknown role raises | smallest impl that passes tests (green) | done 2026-05-31
T-0268 | P4 | agents | docstrings on agents/factory.py public API (why, not what) | every public symbol documented | done 2026-05-31
T-0269 | P4 | agents | type hints on agents/factory.py public signatures (no bare Any) | mypy-clean signatures | done 2026-05-31
T-0270 | P4 | agents | review agents/factory.py for duplication (rule 3) | no copy-paste; shared helpers extracted | done 2026-05-31
T-0271 | P4 | agents | keep agents/factory.py <=150 lines; split helpers if needed | check_line_cap 0 offenders | done 2026-05-31
T-0272 | P4 | agents | integrate agents/factory.py with the SDK / its callers | SDK method or caller wired and tested | done 2026-05-31
T-0273 | P4 | agents | design agents/verdict.py public interface and signatures | interface documented in PRD/PLAN; reviewed | done 2026-05-31
T-0274 | P4 | agents | test(agents): happy-path for Verdict dataclass; validation forbids ties/equal scores | failing test written first (red) | done 2026-05-31
T-0275 | P4 | agents | test(agents): error-path for Verdict dataclass; validation forbids ties/equal scores | raises/handles the error path; test green | done 2026-05-31
T-0276 | P4 | agents | test(agents): edge-case/property test for agents/verdict.py | boundary inputs covered | done 2026-05-31
T-0277 | P4 | agents | implement agents/verdict.py: Verdict dataclass; validation forbids ties/equal scores | smallest impl that passes tests (green) | done 2026-05-31
T-0278 | P4 | agents | docstrings on agents/verdict.py public API (why, not what) | every public symbol documented | done 2026-05-31
T-0279 | P4 | agents | type hints on agents/verdict.py public signatures (no bare Any) | mypy-clean signatures | done 2026-05-31
T-0280 | P4 | agents | review agents/verdict.py for duplication (rule 3) | no copy-paste; shared helpers extracted | done 2026-05-31
T-0281 | P4 | agents | keep agents/verdict.py <=150 lines; split helpers if needed | check_line_cap 0 offenders | done 2026-05-31
T-0282 | P4 | agents | integrate agents/verdict.py with the SDK / its callers | SDK method or caller wired and tested | done 2026-05-31
T-0283 | P4 | agents | design agents/prompts.py public interface and signatures | interface documented in PRD/PLAN; reviewed | done 2026-05-31
T-0284 | P4 | agents | test(agents): happy-path for prompt templates: render Skill + injected context per role | failing test written first (red) | done 2026-05-31
T-0285 | P4 | agents | test(agents): error-path for prompt templates: render Skill + injected context per role | raises/handles the error path; test green | done 2026-05-31
T-0286 | P4 | agents | test(agents): edge-case/property test for agents/prompts.py | boundary inputs covered | done 2026-05-31
T-0287 | P4 | agents | implement agents/prompts.py: prompt templates: render Skill + injected context per role | smallest impl that passes tests (green) | done 2026-05-31
T-0288 | P4 | agents | docstrings on agents/prompts.py public API (why, not what) | every public symbol documented | done 2026-05-31
T-0289 | P4 | agents | type hints on agents/prompts.py public signatures (no bare Any) | mypy-clean signatures | done 2026-05-31
T-0290 | P4 | agents | review agents/prompts.py for duplication (rule 3) | no copy-paste; shared helpers extracted | done 2026-05-31
T-0291 | P4 | agents | keep agents/prompts.py <=150 lines; split helpers if needed | check_line_cap 0 offenders | done 2026-05-31
T-0292 | P4 | agents | integrate agents/prompts.py with the SDK / its callers | SDK method or caller wired and tested | done 2026-05-31
T-0293 | P4 | agents | _render_prompt(context) builds Skill + injected context | task complete and tested | done 2026-05-31
T-0294 | P4 | agents | _invoke() always routes through Gatekeeper.guard | task complete and tested | done 2026-05-31
T-0295 | P4 | agents | _to_message(...) emits a ProtocolMessage | task complete and tested | done 2026-05-31
T-0296 | P4 | agents | DebaterAgent.act produces a ProtocolMessage with a citation within word limit | task complete and tested | done 2026-05-31
T-0297 | P4 | agents | missing-citation turn is flagged | task complete and tested | done 2026-05-31
T-0298 | P4 | agents | JudgeAgent.verdict never ties and always names a winner | task complete and tested | done 2026-05-31
T-0299 | P4 | agents | factory returns ProAgent/ConAgent/JudgeAgent for each role | task complete and tested | done 2026-05-31
T-0300 | P4 | agents | mock runtime + gatekeeper in all agent tests | task complete and tested | done 2026-05-31
T-0301 | P4 | agents | SDK.build_agent(role) wired | task complete and tested | done 2026-05-31
T-0302 | P4 | agents | coverage >=90% on agents/ | task complete and tested | done 2026-05-31
T-0303 | P4 | agents | update TODO; save docs/prompts/004; commit (>=5); push; CI green | task complete and tested | done 2026-05-31

## Phase 5 — JSON IPC protocol

T-0304 | P5 | protocol | design protocol/message.py public interface and signatures | interface documented in PRD/PLAN; reviewed | done 2026-05-31
T-0305 | P5 | protocol | test(protocol): happy-path for pydantic ProtocolMessage with validators | failing test written first (red) | done 2026-05-31
T-0306 | P5 | protocol | test(protocol): error-path for pydantic ProtocolMessage with validators | raises/handles the error path; test green | done 2026-05-31
T-0307 | P5 | protocol | test(protocol): edge-case/property test for protocol/message.py | boundary inputs covered | done 2026-05-31
T-0308 | P5 | protocol | implement protocol/message.py: pydantic ProtocolMessage with validators | smallest impl that passes tests (green) | done 2026-05-31
T-0309 | P5 | protocol | docstrings on protocol/message.py public API (why, not what) | every public symbol documented | done 2026-05-31
T-0310 | P5 | protocol | type hints on protocol/message.py public signatures (no bare Any) | mypy-clean signatures | done 2026-05-31
T-0311 | P5 | protocol | review protocol/message.py for duplication (rule 3) | no copy-paste; shared helpers extracted | done 2026-05-31
T-0312 | P5 | protocol | keep protocol/message.py <=150 lines; split helpers if needed | check_line_cap 0 offenders | done 2026-05-31
T-0313 | P5 | protocol | integrate protocol/message.py with the SDK / its callers | SDK method or caller wired and tested | done 2026-05-31
T-0314 | P5 | protocol | design protocol/routing.py public interface and signatures | interface documented in PRD/PLAN; reviewed | done 2026-05-31
T-0315 | P5 | protocol | test(protocol): happy-path for validate_route + is_through_father audit | failing test written first (red) | done 2026-05-31
T-0316 | P5 | protocol | test(protocol): error-path for validate_route + is_through_father audit | raises/handles the error path; test green | done 2026-05-31
T-0317 | P5 | protocol | test(protocol): edge-case/property test for protocol/routing.py | boundary inputs covered | done 2026-05-31
T-0318 | P5 | protocol | implement protocol/routing.py: validate_route + is_through_father audit | smallest impl that passes tests (green) | done 2026-05-31
T-0319 | P5 | protocol | docstrings on protocol/routing.py public API (why, not what) | every public symbol documented | done 2026-05-31
T-0320 | P5 | protocol | type hints on protocol/routing.py public signatures (no bare Any) | mypy-clean signatures | done 2026-05-31
T-0321 | P5 | protocol | review protocol/routing.py for duplication (rule 3) | no copy-paste; shared helpers extracted | done 2026-05-31
T-0322 | P5 | protocol | keep protocol/routing.py <=150 lines; split helpers if needed | check_line_cap 0 offenders | done 2026-05-31
T-0323 | P5 | protocol | integrate protocol/routing.py with the SDK / its callers | SDK method or caller wired and tested | done 2026-05-31
T-0324 | P5 | protocol | design protocol/serialize.py public interface and signatures | interface documented in PRD/PLAN; reviewed | done 2026-05-31
T-0325 | P5 | protocol | test(protocol): happy-path for to_json/from_json utf-8 helpers | failing test written first (red) | done 2026-05-31
T-0326 | P5 | protocol | test(protocol): error-path for to_json/from_json utf-8 helpers | raises/handles the error path; test green | done 2026-05-31
T-0327 | P5 | protocol | test(protocol): edge-case/property test for protocol/serialize.py | boundary inputs covered | done 2026-05-31
T-0328 | P5 | protocol | implement protocol/serialize.py: to_json/from_json utf-8 helpers | smallest impl that passes tests (green) | done 2026-05-31
T-0329 | P5 | protocol | docstrings on protocol/serialize.py public API (why, not what) | every public symbol documented | done 2026-05-31
T-0330 | P5 | protocol | type hints on protocol/serialize.py public signatures (no bare Any) | mypy-clean signatures | done 2026-05-31
T-0331 | P5 | protocol | review protocol/serialize.py for duplication (rule 3) | no copy-paste; shared helpers extracted | done 2026-05-31
T-0332 | P5 | protocol | keep protocol/serialize.py <=150 lines; split helpers if needed | check_line_cap 0 offenders | done 2026-05-31
T-0333 | P5 | protocol | integrate protocol/serialize.py with the SDK / its callers | SDK method or caller wired and tested | done 2026-05-31
T-0334 | P5 | protocol | design protocol/citation.py public interface and signatures | interface documented in PRD/PLAN; reviewed | done 2026-05-31
T-0335 | P5 | protocol | test(protocol): happy-path for Citation model + citation-count validation | failing test written first (red) | done 2026-05-31
T-0336 | P5 | protocol | test(protocol): error-path for Citation model + citation-count validation | raises/handles the error path; test green | done 2026-05-31
T-0337 | P5 | protocol | test(protocol): edge-case/property test for protocol/citation.py | boundary inputs covered | done 2026-05-31
T-0338 | P5 | protocol | implement protocol/citation.py: Citation model + citation-count validation | smallest impl that passes tests (green) | done 2026-05-31
T-0339 | P5 | protocol | docstrings on protocol/citation.py public API (why, not what) | every public symbol documented | done 2026-05-31
T-0340 | P5 | protocol | type hints on protocol/citation.py public signatures (no bare Any) | mypy-clean signatures | done 2026-05-31
T-0341 | P5 | protocol | review protocol/citation.py for duplication (rule 3) | no copy-paste; shared helpers extracted | done 2026-05-31
T-0342 | P5 | protocol | keep protocol/citation.py <=150 lines; split helpers if needed | check_line_cap 0 offenders | done 2026-05-31
T-0343 | P5 | protocol | integrate protocol/citation.py with the SDK / its callers | SDK method or caller wired and tested | done 2026-05-31
T-0344 | P5 | protocol | valid message round-trips through JSON (serialize->deserialize->equal) | task complete and tested | done 2026-05-31
T-0345 | P5 | protocol | missing required field raises a clear validation error | task complete and tested | done 2026-05-31
T-0346 | P5 | protocol | over-length content fails validation | task complete and tested | done 2026-05-31
T-0347 | P5 | protocol | empty citations[] fails when require_citation_per_turn is true | task complete and tested | done 2026-05-31
T-0348 | P5 | protocol | sender/recipient must be valid roles | task complete and tested | done 2026-05-31
T-0349 | P5 | protocol | child->child (bypassing judge) is rejected by the routing validator | task complete and tested | done 2026-05-31
T-0350 | P5 | protocol | word_count validator matches content | task complete and tested | done 2026-05-31
T-0351 | P5 | protocol | logs store the JSON message | task complete and tested | done 2026-05-31
T-0352 | P5 | protocol | coverage >=90% on protocol/ | task complete and tested | done 2026-05-31
T-0353 | P5 | protocol | update TODO; save docs/prompts/005; commit (>=3); push; CI green | task complete and tested | done 2026-05-31

## Phase 6 — Orchestrator + Watchdog

T-0354 | P6 | orchestration | design orchestration/process_agent.py public interface and signatures | interface documented in PRD/PLAN; reviewed | done 2026-05-31
T-0355 | P6 | orchestration | test(orchestration): happy-path for run one agent in its own multiprocessing.Process with in/out Queues + heartbeat | failing test written first (red) | done 2026-05-31
T-0356 | P6 | orchestration | test(orchestration): error-path for run one agent in its own multiprocessing.Process with in/out Queues + heartbeat | raises/handles the error path; test green | done 2026-05-31
T-0357 | P6 | orchestration | test(orchestration): edge-case/property test for orchestration/process_agent.py | boundary inputs covered | done 2026-05-31
T-0358 | P6 | orchestration | implement orchestration/process_agent.py: run one agent in its own multiprocessing.Process with in/out Queues + heartbeat | smallest impl that passes tests (green) | done 2026-05-31
T-0359 | P6 | orchestration | docstrings on orchestration/process_agent.py public API (why, not what) | every public symbol documented | done 2026-05-31
T-0360 | P6 | orchestration | type hints on orchestration/process_agent.py public signatures (no bare Any) | mypy-clean signatures | done 2026-05-31
T-0361 | P6 | orchestration | review orchestration/process_agent.py for duplication (rule 3) | no copy-paste; shared helpers extracted | done 2026-05-31
T-0362 | P6 | orchestration | keep orchestration/process_agent.py <=150 lines; split helpers if needed | check_line_cap 0 offenders | done 2026-05-31
T-0363 | P6 | orchestration | integrate orchestration/process_agent.py with the SDK / its callers | SDK method or caller wired and tested | done 2026-05-31
T-0364 | P6 | orchestration | design orchestration/orchestrator.py public interface and signatures | interface documented in PRD/PLAN; reviewed | done 2026-05-31
T-0365 | P6 | orchestration | test(orchestration): happy-path for spawn 3 processes; own transcript; run ping loop; persist session JSON | failing test written first (red) | done 2026-05-31
T-0366 | P6 | orchestration | test(orchestration): error-path for spawn 3 processes; own transcript; run ping loop; persist session JSON | raises/handles the error path; test green | done 2026-05-31
T-0367 | P6 | orchestration | test(orchestration): edge-case/property test for orchestration/orchestrator.py | boundary inputs covered | done 2026-05-31
T-0368 | P6 | orchestration | implement orchestration/orchestrator.py: spawn 3 processes; own transcript; run ping loop; persist session JSON | smallest impl that passes tests (green) | done 2026-05-31
T-0369 | P6 | orchestration | docstrings on orchestration/orchestrator.py public API (why, not what) | every public symbol documented | done 2026-05-31
T-0370 | P6 | orchestration | type hints on orchestration/orchestrator.py public signatures (no bare Any) | mypy-clean signatures | done 2026-05-31
T-0371 | P6 | orchestration | review orchestration/orchestrator.py for duplication (rule 3) | no copy-paste; shared helpers extracted | done 2026-05-31
T-0372 | P6 | orchestration | keep orchestration/orchestrator.py <=150 lines; split helpers if needed | check_line_cap 0 offenders | done 2026-05-31
T-0373 | P6 | orchestration | integrate orchestration/orchestrator.py with the SDK / its callers | SDK method or caller wired and tested | done 2026-05-31
T-0374 | P6 | orchestration | design orchestration/loop.py public interface and signatures | interface documented in PRD/PLAN; reviewed | done 2026-05-31
T-0375 | P6 | orchestration | test(orchestration): happy-path for ping-loop helpers and alternation/ordering | failing test written first (red) | done 2026-05-31
T-0376 | P6 | orchestration | test(orchestration): error-path for ping-loop helpers and alternation/ordering | raises/handles the error path; test green | done 2026-05-31
T-0377 | P6 | orchestration | test(orchestration): edge-case/property test for orchestration/loop.py | boundary inputs covered | done 2026-05-31
T-0378 | P6 | orchestration | implement orchestration/loop.py: ping-loop helpers and alternation/ordering | smallest impl that passes tests (green) | done 2026-05-31
T-0379 | P6 | orchestration | docstrings on orchestration/loop.py public API (why, not what) | every public symbol documented | done 2026-05-31
T-0380 | P6 | orchestration | type hints on orchestration/loop.py public signatures (no bare Any) | mypy-clean signatures | done 2026-05-31
T-0381 | P6 | orchestration | review orchestration/loop.py for duplication (rule 3) | no copy-paste; shared helpers extracted | done 2026-05-31
T-0382 | P6 | orchestration | keep orchestration/loop.py <=150 lines; split helpers if needed | check_line_cap 0 offenders | done 2026-05-31
T-0383 | P6 | orchestration | integrate orchestration/loop.py with the SDK / its callers | SDK method or caller wired and tested | done 2026-05-31
T-0384 | P6 | orchestration | design orchestration/watchdog.py public interface and signatures | interface documented in PRD/PLAN; reviewed | done 2026-05-31
T-0385 | P6 | orchestration | test(orchestration): happy-path for timeouts + heartbeat monitor + kill/restart with context replay | failing test written first (red) | done 2026-05-31
T-0386 | P6 | orchestration | test(orchestration): error-path for timeouts + heartbeat monitor + kill/restart with context replay | raises/handles the error path; test green | done 2026-05-31
T-0387 | P6 | orchestration | test(orchestration): edge-case/property test for orchestration/watchdog.py | boundary inputs covered | done 2026-05-31
T-0388 | P6 | orchestration | implement orchestration/watchdog.py: timeouts + heartbeat monitor + kill/restart with context replay | smallest impl that passes tests (green) | done 2026-05-31
T-0389 | P6 | orchestration | docstrings on orchestration/watchdog.py public API (why, not what) | every public symbol documented | done 2026-05-31
T-0390 | P6 | orchestration | type hints on orchestration/watchdog.py public signatures (no bare Any) | mypy-clean signatures | done 2026-05-31
T-0391 | P6 | orchestration | review orchestration/watchdog.py for duplication (rule 3) | no copy-paste; shared helpers extracted | done 2026-05-31
T-0392 | P6 | orchestration | keep orchestration/watchdog.py <=150 lines; split helpers if needed | check_line_cap 0 offenders | done 2026-05-31
T-0393 | P6 | orchestration | integrate orchestration/watchdog.py with the SDK / its callers | SDK method or caller wired and tested | done 2026-05-31
T-0394 | P6 | orchestration | design orchestration/transcript.py public interface and signatures | interface documented in PRD/PLAN; reviewed | done 2026-05-31
T-0395 | P6 | orchestration | test(orchestration): happy-path for incremental session_NNN.json writer + schema | failing test written first (red) | done 2026-05-31
T-0396 | P6 | orchestration | test(orchestration): error-path for incremental session_NNN.json writer + schema | raises/handles the error path; test green | done 2026-05-31
T-0397 | P6 | orchestration | test(orchestration): edge-case/property test for orchestration/transcript.py | boundary inputs covered | done 2026-05-31
T-0398 | P6 | orchestration | implement orchestration/transcript.py: incremental session_NNN.json writer + schema | smallest impl that passes tests (green) | done 2026-05-31
T-0399 | P6 | orchestration | docstrings on orchestration/transcript.py public API (why, not what) | every public symbol documented | done 2026-05-31
T-0400 | P6 | orchestration | type hints on orchestration/transcript.py public signatures (no bare Any) | mypy-clean signatures | done 2026-05-31
T-0401 | P6 | orchestration | review orchestration/transcript.py for duplication (rule 3) | no copy-paste; shared helpers extracted | done 2026-05-31
T-0402 | P6 | orchestration | keep orchestration/transcript.py <=150 lines; split helpers if needed | check_line_cap 0 offenders | done 2026-05-31
T-0403 | P6 | orchestration | integrate orchestration/transcript.py with the SDK / its callers | SDK method or caller wired and tested | done 2026-05-31
T-0404 | P6 | orchestration | design orchestration/summary.py public interface and signatures | interface documented in PRD/PLAN; reviewed | done 2026-05-31
T-0405 | P6 | orchestration | test(orchestration): happy-path for running-summary builder for Context Engineering | failing test written first (red) | done 2026-05-31
T-0406 | P6 | orchestration | test(orchestration): error-path for running-summary builder for Context Engineering | raises/handles the error path; test green | done 2026-05-31
T-0407 | P6 | orchestration | test(orchestration): edge-case/property test for orchestration/summary.py | boundary inputs covered | done 2026-05-31
T-0408 | P6 | orchestration | implement orchestration/summary.py: running-summary builder for Context Engineering | smallest impl that passes tests (green) | done 2026-05-31
T-0409 | P6 | orchestration | docstrings on orchestration/summary.py public API (why, not what) | every public symbol documented | done 2026-05-31
T-0410 | P6 | orchestration | type hints on orchestration/summary.py public signatures (no bare Any) | mypy-clean signatures | done 2026-05-31
T-0411 | P6 | orchestration | review orchestration/summary.py for duplication (rule 3) | no copy-paste; shared helpers extracted | done 2026-05-31
T-0412 | P6 | orchestration | keep orchestration/summary.py <=150 lines; split helpers if needed | check_line_cap 0 offenders | done 2026-05-31
T-0413 | P6 | orchestration | integrate orchestration/summary.py with the SDK / its callers | SDK method or caller wired and tested | done 2026-05-31
T-0414 | P6 | orchestration | Context Engineering: select opponent last turn + running summary into next prompt | task complete and tested | done 2026-05-31
T-0415 | P6 | orchestration | evict old raw turns to keep prompts small | task complete and tested | done 2026-05-31
T-0416 | P6 | orchestration | loop produces exactly pings_per_side turns per side | task complete and tested | done 2026-05-31
T-0417 | P6 | orchestration | every message routed through the judge (assert is_through_father) | task complete and tested | done 2026-05-31
T-0418 | P6 | orchestration | simulated dead process detected and restarted (<= max_restarts_per_agent) | task complete and tested | done 2026-05-31
T-0419 | P6 | orchestration | a hung call hits the timeout | task complete and tested | done 2026-05-31
T-0420 | P6 | orchestration | transcript file written incrementally to transcripts/session_NNN.json | task complete and tested | done 2026-05-31
T-0421 | P6 | orchestration | verdict requested from judge on completion and appended | task complete and tested | done 2026-05-31
T-0422 | P6 | orchestration | mock agents return canned ProtocolMessages in unit tests | task complete and tested | done 2026-05-31
T-0423 | P6 | orchestration | integration test (marker live) runs a 1-ping real debate, skipped in CI | task complete and tested | done 2026-05-31
T-0424 | P6 | orchestration | SDK.run_debate() returns transcript path + verdict | task complete and tested | done 2026-05-31
T-0425 | P6 | orchestration | watchdog logs every restart | task complete and tested | done 2026-05-31
T-0426 | P6 | orchestration | restart exhaustion handled cleanly | task complete and tested | done 2026-05-31
T-0427 | P6 | orchestration | coverage >=85% on orchestration/ | task complete and tested | done 2026-05-31
T-0428 | P6 | orchestration | update TODO; save docs/prompts/006; commit (>=5); push; CI green | task complete and tested | done 2026-05-31

## Phase 7 — Judge logic

T-0429 | P7 | judge | design agents/judge.py (enforce) public interface and signatures | interface documented in PRD/PLAN; reviewed | todo
T-0430 | P7 | judge | test(judge): happy-path for reject citation-less/over-length/non-rebutting/agreeing turns | failing test written first (red) | todo
T-0431 | P7 | judge | test(judge): error-path for reject citation-less/over-length/non-rebutting/agreeing turns | raises/handles the error path; test green | todo
T-0432 | P7 | judge | test(judge): edge-case/property test for agents/judge.py (enforce) | boundary inputs covered | todo
T-0433 | P7 | judge | implement agents/judge.py (enforce): reject citation-less/over-length/non-rebutting/agreeing turns | smallest impl that passes tests (green) | todo
T-0434 | P7 | judge | docstrings on agents/judge.py (enforce) public API (why, not what) | every public symbol documented | todo
T-0435 | P7 | judge | type hints on agents/judge.py (enforce) public signatures (no bare Any) | mypy-clean signatures | todo
T-0436 | P7 | judge | review agents/judge.py (enforce) for duplication (rule 3) | no copy-paste; shared helpers extracted | todo
T-0437 | P7 | judge | keep agents/judge.py (enforce) <=150 lines; split helpers if needed | check_line_cap 0 offenders | todo
T-0438 | P7 | judge | design agents/judge.py (score_turn) public interface and signatures | interface documented in PRD/PLAN; reviewed | todo
T-0439 | P7 | judge | test(judge): happy-path for rubric scores clarity/evidence/rebuttal/rhetoric | failing test written first (red) | todo
T-0440 | P7 | judge | test(judge): error-path for rubric scores clarity/evidence/rebuttal/rhetoric | raises/handles the error path; test green | todo
T-0441 | P7 | judge | test(judge): edge-case/property test for agents/judge.py (score_turn) | boundary inputs covered | todo
T-0442 | P7 | judge | implement agents/judge.py (score_turn): rubric scores clarity/evidence/rebuttal/rhetoric | smallest impl that passes tests (green) | todo
T-0443 | P7 | judge | docstrings on agents/judge.py (score_turn) public API (why, not what) | every public symbol documented | todo
T-0444 | P7 | judge | type hints on agents/judge.py (score_turn) public signatures (no bare Any) | mypy-clean signatures | todo
T-0445 | P7 | judge | review agents/judge.py (score_turn) for duplication (rule 3) | no copy-paste; shared helpers extracted | todo
T-0446 | P7 | judge | keep agents/judge.py (score_turn) <=150 lines; split helpers if needed | check_line_cap 0 offenders | todo
T-0447 | P7 | judge | design agents/judge.py (verdict) public interface and signatures | interface documented in PRD/PLAN; reviewed | todo
T-0448 | P7 | judge | test(judge): happy-path for aggregate scores, pick winner, differential score, justification | failing test written first (red) | todo
T-0449 | P7 | judge | test(judge): error-path for aggregate scores, pick winner, differential score, justification | raises/handles the error path; test green | todo
T-0450 | P7 | judge | test(judge): edge-case/property test for agents/judge.py (verdict) | boundary inputs covered | todo
T-0451 | P7 | judge | implement agents/judge.py (verdict): aggregate scores, pick winner, differential score, justification | smallest impl that passes tests (green) | todo
T-0452 | P7 | judge | docstrings on agents/judge.py (verdict) public API (why, not what) | every public symbol documented | todo
T-0453 | P7 | judge | type hints on agents/judge.py (verdict) public signatures (no bare Any) | mypy-clean signatures | todo
T-0454 | P7 | judge | review agents/judge.py (verdict) for duplication (rule 3) | no copy-paste; shared helpers extracted | todo
T-0455 | P7 | judge | keep agents/judge.py (verdict) <=150 lines; split helpers if needed | check_line_cap 0 offenders | todo
T-0456 | P7 | judge | enforce: citation-less turn rejected with redo request | task complete and tested | todo
T-0457 | P7 | judge | enforce: over-length turn rejected | task complete and tested | todo
T-0458 | P7 | judge | enforce: non-rebutting turn flagged | task complete and tested | todo
T-0459 | P7 | judge | enforce: 'I agree with you' drift triggers intervention | task complete and tested | todo
T-0460 | P7 | judge | score_turn: persuasion only (truth irrelevant; lies allowed) | task complete and tested | todo
T-0461 | P7 | judge | verdict: winner always named with unequal scores | task complete and tested | todo
T-0462 | P7 | judge | verdict: justification non-empty and references specific turns | task complete and tested | todo
T-0463 | P7 | judge | verdict: close scores broken by rebuttal quality | task complete and tested | todo
T-0464 | P7 | judge | Verdict validation rejects equal scores / 'tie' | task complete and tested | todo
T-0465 | P7 | judge | SDK.last_verdict() reads the latest transcript verdict | task complete and tested | todo
T-0466 | P7 | judge | coverage >=90% on judge/verdict | task complete and tested | todo
T-0467 | P7 | judge | update TODO; save docs/prompts/007; commit (>=4); push; CI green | task complete and tested | todo

## Phase 8 — Terminal menu + CLI

T-0468 | P8 | cli | design cli/menu.py public interface and signatures | interface documented in PRD/PLAN; reviewed | todo
T-0469 | P8 | cli | test(cli): happy-path for Menu rendering with rich; options call SDK | failing test written first (red) | todo
T-0470 | P8 | cli | test(cli): error-path for Menu rendering with rich; options call SDK | raises/handles the error path; test green | todo
T-0471 | P8 | cli | test(cli): edge-case/property test for cli/menu.py | boundary inputs covered | todo
T-0472 | P8 | cli | implement cli/menu.py: Menu rendering with rich; options call SDK | smallest impl that passes tests (green) | todo
T-0473 | P8 | cli | docstrings on cli/menu.py public API (why, not what) | every public symbol documented | todo
T-0474 | P8 | cli | type hints on cli/menu.py public signatures (no bare Any) | mypy-clean signatures | todo
T-0475 | P8 | cli | review cli/menu.py for duplication (rule 3) | no copy-paste; shared helpers extracted | todo
T-0476 | P8 | cli | keep cli/menu.py <=150 lines; split helpers if needed | check_line_cap 0 offenders | todo
T-0477 | P8 | cli | design cli/actions.py public interface and signatures | interface documented in PRD/PLAN; reviewed | todo
T-0478 | P8 | cli | test(cli): happy-path for menu action handlers calling the SDK | failing test written first (red) | todo
T-0479 | P8 | cli | test(cli): error-path for menu action handlers calling the SDK | raises/handles the error path; test green | todo
T-0480 | P8 | cli | test(cli): edge-case/property test for cli/actions.py | boundary inputs covered | todo
T-0481 | P8 | cli | implement cli/actions.py: menu action handlers calling the SDK | smallest impl that passes tests (green) | todo
T-0482 | P8 | cli | docstrings on cli/actions.py public API (why, not what) | every public symbol documented | todo
T-0483 | P8 | cli | type hints on cli/actions.py public signatures (no bare Any) | mypy-clean signatures | todo
T-0484 | P8 | cli | review cli/actions.py for duplication (rule 3) | no copy-paste; shared helpers extracted | todo
T-0485 | P8 | cli | keep cli/actions.py <=150 lines; split helpers if needed | check_line_cap 0 offenders | todo
T-0486 | P8 | cli | design cli/main.py public interface and signatures | interface documented in PRD/PLAN; reviewed | todo
T-0487 | P8 | cli | test(cli): happy-path for argparse entry: menu/run/verdict/cost/logs subcommands | failing test written first (red) | todo
T-0488 | P8 | cli | test(cli): error-path for argparse entry: menu/run/verdict/cost/logs subcommands | raises/handles the error path; test green | todo
T-0489 | P8 | cli | test(cli): edge-case/property test for cli/main.py | boundary inputs covered | todo
T-0490 | P8 | cli | implement cli/main.py: argparse entry: menu/run/verdict/cost/logs subcommands | smallest impl that passes tests (green) | todo
T-0491 | P8 | cli | docstrings on cli/main.py public API (why, not what) | every public symbol documented | todo
T-0492 | P8 | cli | type hints on cli/main.py public signatures (no bare Any) | mypy-clean signatures | todo
T-0493 | P8 | cli | review cli/main.py for duplication (rule 3) | no copy-paste; shared helpers extracted | todo
T-0494 | P8 | cli | keep cli/main.py <=150 lines; split helpers if needed | check_line_cap 0 offenders | todo
T-0495 | P8 | cli | design cli/render.py public interface and signatures | interface documented in PRD/PLAN; reviewed | todo
T-0496 | P8 | cli | test(cli): happy-path for rich rendering helpers (tables, panels) for menu output | failing test written first (red) | todo
T-0497 | P8 | cli | test(cli): error-path for rich rendering helpers (tables, panels) for menu output | raises/handles the error path; test green | todo
T-0498 | P8 | cli | test(cli): edge-case/property test for cli/render.py | boundary inputs covered | todo
T-0499 | P8 | cli | implement cli/render.py: rich rendering helpers (tables, panels) for menu output | smallest impl that passes tests (green) | todo
T-0500 | P8 | cli | docstrings on cli/render.py public API (why, not what) | every public symbol documented | todo
T-0501 | P8 | cli | type hints on cli/render.py public signatures (no bare Any) | mypy-clean signatures | todo
T-0502 | P8 | cli | review cli/render.py for duplication (rule 3) | no copy-paste; shared helpers extracted | todo
T-0503 | P8 | cli | keep cli/render.py <=150 lines; split helpers if needed | check_line_cap 0 offenders | todo
T-0504 | P8 | cli | render the 8-option menu ([1]..[7],[0]) | task complete and tested | todo
T-0505 | P8 | cli | each option calls the right SDK method | task complete and tested | todo
T-0506 | P8 | cli | invalid input re-prompts gracefully | task complete and tested | todo
T-0507 | P8 | cli | --help lists subcommands | task complete and tested | todo
T-0508 | P8 | cli | menu launches the interactive loop (default subcommand) | task complete and tested | todo
T-0509 | P8 | cli | wire cosmos77-debate script | task complete and tested | todo
T-0510 | P8 | cli | monkeypatch input() to drive menu tests; SDK mocked | task complete and tested | todo
T-0511 | P8 | cli | cosmos77-debate --help and menu work after uv sync | task complete and tested | todo
T-0512 | P8 | cli | update TODO; save docs/prompts/008; commit (>=2); push; CI green | task complete and tested | todo

## Phase 9 — Real debate run, transcript, diagrams, cost

T-0513 | P9 | run | run full debate (10 pings/side) on configured topic via cosmos77-debate run | session_001.json committed with verdict | todo
T-0514 | P9 | run | debate completes with a no-tie verdict | session_001.json committed with verdict | todo
T-0515 | P9 | run | write transcripts/session_001.json and commit it | session_001.json committed with verdict | todo
T-0516 | P9 | run | verify every debater turn has non-empty citations | session_001.json committed with verdict | todo
T-0517 | P9 | run | lower pings + note in README if budget cap trips, then rerun | session_001.json committed with verdict | todo
T-0518 | P9 | diagrams | docs/diagrams/architecture.mmd (class diagram) | diagrams committed | todo
T-0519 | P9 | diagrams | docs/diagrams/sequence.mmd (one full ping) | diagrams committed | todo
T-0520 | P9 | diagrams | render architecture.png into assets/ | diagrams committed | todo
T-0521 | P9 | diagrams | render sequence.png into assets/ | diagrams committed | todo
T-0522 | P9 | diagrams | commit .mmd + rendered PNGs (or note if renderer unavailable) | diagrams committed | todo
T-0523 | P9 | cost | cost_report: total USD spent (sum per-call total_cost_usd) | cost report committed | todo
T-0524 | P9 | cost | cost_report: input/output tokens | cost report committed | todo
T-0525 | P9 | cost | cost_report: cost per ping | cost report committed | todo
T-0526 | P9 | cost | cost_report: projected cost at 10 vs 5 pings | cost report committed | todo
T-0527 | P9 | cost | save transcripts/session_001_cost.json + human-readable table | cost report committed | todo
T-0528 | P9 | assets | screenshot: the menu (assets/) | assets committed (manual screenshots) | todo
T-0529 | P9 | assets | screenshot: a live debate turn (assets/) | assets committed (manual screenshots) | todo
T-0530 | P9 | assets | screenshot: the final verdict (assets/) | assets committed (manual screenshots) | todo
T-0531 | P9 | assets | screenshot: the cost report (assets/) | assets committed (manual screenshots) | todo
T-0532 | P9 | assets | update TODO; save docs/prompts/009; commit (>=4); push; CI green | assets committed (manual screenshots) | todo

## Phase 10 — README lab report

T-0533 | P10 | readme | README: title + authors + course + date | README section complete | todo
T-0534 | P10 | readme | README: abstract (topic, architecture, who won and why) | README section complete | todo
T-0535 | P10 | readme | README: the debate task + link PRD + positions | README section complete | todo
T-0536 | P10 | readme | README: architecture (embed architecture.png + sequence.png) | README section complete | todo
T-0537 | P10 | readme | README: quickstart (uv, claude CLI Max login, no key) | README section complete | todo
T-0538 | P10 | readme | README: usage (every menu option + CLI subcommand + screenshots) | README section complete | todo
T-0539 | P10 | readme | README: configuration guide (every setup/gatekeeper key) | README section complete | todo
T-0540 | P10 | readme | README: the Skills (Pro/Con/Judge descriptions; why they differ) | README section complete | todo
T-0541 | P10 | readme | README: Session 1 full JSON dialogue + verdict + interpretation paragraph | README section complete | todo
T-0542 | P10 | readme | README: engineering (watchdog, gatekeeper, FIFO logs, SDK, OOP, TDD, CI badge) | README section complete | todo
T-0543 | P10 | readme | README: cost analysis (embed Phase-9 cost report) | README section complete | todo
T-0544 | P10 | readme | README: how to extend (link PRD_extension_points) | README section complete | todo
T-0545 | P10 | readme | README: how we used AI agents (docs/prompts pointer + vibe-coding narrative) | README section complete | todo
T-0546 | P10 | readme | README: limitations & future work | README section complete | todo
T-0547 | P10 | readme | README: testing & quality (pytest >=85%, ruff, line-cap, CI) | README section complete | todo
T-0548 | P10 | readme | README: license + acknowledgements & citations | README section complete | todo
T-0549 | P10 | readme | README: self-assessment vs 17 rules + A1-A15; recommend self-score 85 | README section complete | todo
T-0550 | P10 | readme | README: >=250 lines, >=5 embedded images; update dates + repo URL | README section complete | todo
T-0551 | P10 | readme | update TODO; save docs/prompts/010; commit (>=2); push; CI green | README section complete | todo

## Phase 11 — Final QA gauntlet

T-0552 | P11 | qa | ruff check . zero | gate green | todo
T-0553 | P11 | qa | ruff format --check . clean | gate green | todo
T-0554 | P11 | qa | pytest --cov-fail-under=85 green (unit + non-live integration) | gate green | todo
T-0555 | P11 | qa | check_line_cap.py 0 offenders | gate green | todo
T-0556 | P11 | qa | integration: full loop (mocked) produces 10 pings/side | gate green | todo
T-0557 | P11 | qa | integration: every message routed through judge | gate green | todo
T-0558 | P11 | qa | integration: watchdog restarts a killed process | gate green | todo
T-0559 | P11 | qa | integration: verdict never a tie | gate green | todo
T-0560 | P11 | qa | integration: SDK end-to-end | gate green | todo
T-0561 | P11 | qa | integration: menu via monkeypatched input | gate green | todo
T-0562 | P11 | qa | re-run real debate; session_001.json has no-tie verdict + citations | gate green | todo
T-0563 | P11 | qa | secrets: no .env tracked; no keys in src; .env.example present | gate green | todo
T-0564 | P11 | qa | uv lock --check passes; uv.lock committed | gate green | todo
T-0565 | P11 | qa | CLAUDE.md unchanged from Phase 0 except whitespace | gate green | todo
T-0566 | P11 | qa | no wip/tmp/fixup commits; >=30 commits; both authors in shortlog | gate green | todo
T-0567 | P11 | qa | GitHub Actions green on latest main | gate green | todo
T-0568 | P11 | qa | reproducibility: fresh clone -> uv sync -> pytest -> --help all work | gate green | todo
T-0569 | P11 | qa | docs/prompts 000-011 present; CHANGELOG full [1.00] entry | gate green | todo
T-0570 | P11 | qa | save docs/prompts/011; commit fixes; push; CI green | gate green | todo
T-0571 | P11 | acceptance | audit acceptance criterion A1: map to a passing test or committed artifact in docs/ACCEPTANCE.md | A-id mapped and satisfied | todo
T-0572 | P11 | acceptance | audit acceptance criterion A2: map to a passing test or committed artifact in docs/ACCEPTANCE.md | A-id mapped and satisfied | todo
T-0573 | P11 | acceptance | audit acceptance criterion A3: map to a passing test or committed artifact in docs/ACCEPTANCE.md | A-id mapped and satisfied | todo
T-0574 | P11 | acceptance | audit acceptance criterion A4: map to a passing test or committed artifact in docs/ACCEPTANCE.md | A-id mapped and satisfied | todo
T-0575 | P11 | acceptance | audit acceptance criterion A5: map to a passing test or committed artifact in docs/ACCEPTANCE.md | A-id mapped and satisfied | todo
T-0576 | P11 | acceptance | audit acceptance criterion A6: map to a passing test or committed artifact in docs/ACCEPTANCE.md | A-id mapped and satisfied | todo
T-0577 | P11 | acceptance | audit acceptance criterion A7: map to a passing test or committed artifact in docs/ACCEPTANCE.md | A-id mapped and satisfied | todo
T-0578 | P11 | acceptance | audit acceptance criterion A8: map to a passing test or committed artifact in docs/ACCEPTANCE.md | A-id mapped and satisfied | todo
T-0579 | P11 | acceptance | audit acceptance criterion A9: map to a passing test or committed artifact in docs/ACCEPTANCE.md | A-id mapped and satisfied | todo
T-0580 | P11 | acceptance | audit acceptance criterion A10: map to a passing test or committed artifact in docs/ACCEPTANCE.md | A-id mapped and satisfied | todo
T-0581 | P11 | acceptance | audit acceptance criterion A11: map to a passing test or committed artifact in docs/ACCEPTANCE.md | A-id mapped and satisfied | todo
T-0582 | P11 | acceptance | audit acceptance criterion A12: map to a passing test or committed artifact in docs/ACCEPTANCE.md | A-id mapped and satisfied | todo
T-0583 | P11 | acceptance | audit acceptance criterion A13: map to a passing test or committed artifact in docs/ACCEPTANCE.md | A-id mapped and satisfied | todo
T-0584 | P11 | acceptance | audit acceptance criterion A14: map to a passing test or committed artifact in docs/ACCEPTANCE.md | A-id mapped and satisfied | todo
T-0585 | P11 | acceptance | audit acceptance criterion A15: map to a passing test or committed artifact in docs/ACCEPTANCE.md | A-id mapped and satisfied | todo

## Phase 12 — Cover PDF + tag + release + submit

T-0586 | P12 | submit | retarget generate_cover_pdf.py: exercise number = 2 | submission ready | todo
T-0587 | P12 | submit | retarget generate_cover_pdf.py: ex02 repo URL | submission ready | todo
T-0588 | P12 | submit | add --exercise-number flag (and split file to stay <=150 lines) | submission ready | todo
T-0589 | P12 | submit | keep/confirm test_cover_pdf.py (mock conversion, assert exercise number 2 + ex02 URL) | submission ready | todo
T-0590 | P12 | submit | run generator to produce ~/COSMOS77/HW2/COSMOS77-ex02.pdf | submission ready | todo
T-0591 | P12 | submit | verify PDF: filename, layout untouched, fields filled, exercise number 2, ex02 URL | submission ready | todo
T-0592 | P12 | submit | ensure *.pdf gitignored; commit script/test only | submission ready | todo
T-0593 | P12 | submit | git tag -a v1.00 and push tag | submission ready | todo
T-0594 | P12 | submit | gh release create v1.00 with CHANGELOG notes | submission ready | todo
T-0595 | P12 | submit | print final summary (repo URL, tag, PDF path, manual web-UI steps) | submission ready | todo
T-0596 | P12 | submit | verify cover PDF %PDF magic bytes after conversion | submission ready | todo
T-0597 | P12 | submit | confirm docx->pdf fallback chain (docx2pdf -> soffice -> libreoffice) | submission ready | todo
T-0598 | P12 | submit | confirm self-score 85 appears on cover AND README | submission ready | todo
T-0599 | P12 | submit | final master-checklist eyeball (playbook §16) before upload | submission ready | todo
T-0600 | P12 | submit | save docs/prompts/012; commit; push | submission ready | todo
T-0601 | P12 | submit | MANUAL: collaborator/visibility (public ok) + Moodle upload by both partners | submission ready | todo
T-0602 | P9 | run | check mermaid CLI availability (npx @mermaid-js/mermaid-cli) before render | run artifact validated | todo
T-0603 | P9 | run | validate session_001.json against the transcript schema | run artifact validated | todo
T-0604 | P9 | run | assert exactly 10 pings per side in session_001.json | run artifact validated | todo
T-0605 | P9 | run | confirm verdict winner + differential score present in transcript | run artifact validated | todo
T-0606 | P10 | readme | embed BADGES.md badges at the top of README | README polish complete | todo
T-0607 | P10 | readme | verify README image links resolve to assets/ files | README polish complete | todo
T-0608 | P10 | readme | proofread README for English-only and PC language | README polish complete | todo
