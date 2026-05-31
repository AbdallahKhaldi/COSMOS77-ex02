# TODO — COSMOS77-ex02

Single source of truth for outstanding work. Format (one task per line, so
`grep -c '^T-' docs/TODO.md` counts them):

```
T-NNNN | <phase> | <area> | <description> | <definition-of-done> | <status>
```

**Phase 1 expands this list to ≥ 600 granular tasks** (per playbook §3, task 15),
distributed across P0–P12. This Phase-0 seed tracks the bootstrap tasks only so
the commits have real IDs to reference; later phases append their own ranges.

## Phase 0 — Repo bootstrap (done 2026-05-31)

T-0001 | P0 | repo | git init -b main, set user identity, add origin remote | `git remote -v` shows the ex02 URL; branch is `main` | done 2026-05-31
T-0002 | P0 | repo | create directory layout (src package + subpackages, tests, docs, config, logs, transcripts, assets) | tree matches playbook §2.2 task 1 | done 2026-05-31
T-0003 | P0 | repo | package skeleton: __init__.py with module docstrings for every subpackage | `python -c "import cosmos77_ex02"` succeeds | done 2026-05-31
T-0004 | P0 | build | pyproject.toml: name cosmos77-ex02, version 1.00, deps, dev group, script, ruff/coverage/pytest config | `uv sync` resolves; ruff reads config | done 2026-05-31
T-0005 | P0 | build | .python-version = 3.11 | file present | done 2026-05-31
T-0006 | P0 | repo | .gitignore: env, caches, logs, transcripts, pdf; keep .gitkeep + session_001 | `git status` ignores .venv/.env | done 2026-05-31
T-0007 | P0 | cyber | .env.example placeholders only (claude CLI login; no keys) | no real secrets; `.env` gitignored | done 2026-05-31
T-0008 | P0 | config | config/setup.json (debate/runtime/orchestration/paths) | valid JSON; version 1.00 | done 2026-05-31
T-0009 | P0 | config | config/gatekeeper.json (budget cap 5.00) | valid JSON; version 1.00 | done 2026-05-31
T-0010 | P0 | config | config/logging_config.json (FIFO 20×500 handler reference) | valid JSON; dictConfig version 1 | done 2026-05-31
T-0011 | P0 | governance | CLAUDE.md (17 rules verbatim from playbook §17) | matches Appendix A | done 2026-05-31
T-0012 | P0 | docs | README.md placeholder (full report in Phase 10) | renders; links resolve | done 2026-05-31
T-0013 | P0 | governance | LICENSE (MIT, 2026, both authors) | present | done 2026-05-31
T-0014 | P0 | governance | CHANGELOG.md Keep-a-Changelog [1.00] entry | present | done 2026-05-31
T-0015 | P0 | governance | CONTRIBUTING.md (rules, commits, gates, prompt-log) | present | done 2026-05-31
T-0016 | P0 | governance | BADGES.md (ex02 CI badge + python/license/uv/coverage) | present | done 2026-05-31
T-0017 | P0 | quality | scripts/check_line_cap.py (≤150 enforcement, ≤80 lines) | `python scripts/check_line_cap.py` → 0 offenders | done 2026-05-31
T-0018 | P0 | quality | scripts/generate_cover_pdf.py (ported; retargeted in Phase 12) | imports parse; lints clean | done 2026-05-31
T-0019 | P0 | quality | .pre-commit-config.yaml (ruff + std hooks + local line-cap) | `pre-commit run` wiring valid | done 2026-05-31
T-0020 | P0 | ci | .github/workflows/ci.yml (uv sync --frozen, ruff, line-cap, pytest cov gate, exclude live) | workflow valid YAML | done 2026-05-31
T-0021 | P0 | core | constants.py (ROLES, TURN_TYPES, DEFAULT_ENCODING) | importable; ≤30 lines | done 2026-05-31
T-0022 | P0 | test | tests/unit/test_constants.py + conftest.py harness | `pytest` collects ≥1 test; constants 100% covered | done 2026-05-31
T-0023 | P0 | docs | docs PRD/PLAN placeholders (14 stubs) for Phase 1 | files present with per-file scope | done 2026-05-31
T-0024 | P0 | build | uv sync → .venv + uv.lock committed | both exist; `uv lock --check` passes | done 2026-05-31
T-0025 | P0 | quality | ruff check zero + ruff format clean + line-cap 0 + pytest ≥85% | all gates green locally | done 2026-05-31
T-0026 | P0 | quality | pre-commit installed in the local repo | `.git/hooks/pre-commit` present | done 2026-05-31
T-0027 | P0 | docs | docs/prompts/000_phase0_bootstrap.md (prompt + summary) | present | done 2026-05-31
T-0028 | P0 | ci | conventional commits (both authors) + push origin main + CI green | Actions green on main | done 2026-05-31

## Phases 1–12 — pending

T-0100 | P1 | docs | Phase 1 expands TODO to ≥600 tasks; writes PRD/PLAN/12 mechanism PRDs | playbook §3 verification passes | todo
T-0200 | P2 | shared | Port Config/version/logging(FIFO)/Gatekeeper from HW1 + SDK skeleton | playbook §4 verification passes | todo
T-0300 | P3 | runtime | `claude -p` JSON wrapper (argv, parse, timeout), mocked | playbook §5 verification passes | todo
T-0400 | P4 | agents | Agent hierarchy + 3 distinct Skills | playbook §6 verification passes | todo
T-0500 | P5 | protocol | pydantic ProtocolMessage + routing + serialize | playbook §7 verification passes | todo
T-0600 | P6 | orchestration | Orchestrator + per-agent process + Watchdog | playbook §8 verification passes | todo
T-0700 | P7 | judge | enforce/score/no-tie verdict | playbook §9 verification passes | todo
T-0800 | P8 | cli | terminal menu + argparse entry | playbook §10 verification passes | todo
T-0900 | P9 | run | real debate, transcript, diagrams, cost report | playbook §11 verification passes | todo
T-1000 | P10 | docs | README lab report | playbook §12 verification passes | todo
T-1100 | P11 | qa | acceptance audit + ACCEPTANCE.md, all gates green | playbook §13 verification passes | todo
T-1200 | P12 | submit | cover PDF + tag v1.00 + release + Moodle | playbook §14 verification passes | todo
