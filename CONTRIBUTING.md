# Contributing to COSMOS77-ex02

This document captures the working agreement for the two student contributors
(Abdallah Khaldi and Tasneem Natour) and any future maintainers. It mirrors the
17 binding rules in [CLAUDE.md](CLAUDE.md) and the master playbook
(`../CLAUDE_CODE_PLAYBOOK.md`).

## Local setup

```bash
# Install uv (one-time)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Sync the locked environment
uv sync

# Install pre-commit hooks
uv run pre-commit install
```

`uv sync` materialises `.venv/` and `uv.lock`. **Never** invoke `pip`,
`python -m venv`, or `python script.py` directly — every Python entry point
goes through `uv run` (rule 5).

The LLM backend is the **`claude` CLI** authenticated with a Claude Max/Pro
subscription (`claude` → `/login`). It is an **external prerequisite**, not a
pip dependency, and needs **no API key** (rule 9).

## Branching

| Prefix      | Purpose                                                |
|-------------|--------------------------------------------------------|
| `feat/`     | New capability (agent, skill, protocol, CLI command, …)|
| `fix/`      | Bug fix that does not change the public surface        |
| `docs/`     | README, PRD, PLAN, TODO, prompt log changes            |
| `chore/`    | Tooling, CI, configs, dependency bumps                 |
| `refactor/` | Internal restructuring with no behaviour change        |
| `test/`     | Adding or hardening tests only                         |

Always branch off `main`.

## Commits

Conventional Commits is mandatory (rule 11):

```
type(scope): short imperative summary

Optional body explaining the *why* and referencing the TODO ID.

Closes T-NNNN
```

Examples: `feat(agents): add JudgeAgent.relay`, `test(protocol): cover routing
rejection`, `docs(plan): add ADR-003 on multiprocessing IPC`. Multiple commits
per phase are encouraged; mega-commits (`wip`, `tmp`, `fixup`) are forbidden —
the grading agent flags them. This is a two-person team, so commits are
authored by both partners and carry `Co-Authored-By` trailers.

## Quality gates

Before pushing, run locally:

```bash
uv run ruff check .                 # zero issues
uv run ruff format --check .        # zero diffs
uv run python scripts/check_line_cap.py
uv run pytest -m "not live" --cov-fail-under=85
```

The same gates run in [GitHub Actions](.github/workflows/ci.yml) on every push
and pull request to `main`. A red CI bar blocks merges. **No test ever invokes
the real `claude` binary** — all LLM/subprocess/network I/O is mocked (rule 6,
acceptance A9). Live end-to-end checks are marked `live` and excluded from CI.

## Test-driven development

Every public function or class lands tests **before** the implementation:

1. **Red** — write a failing test that captures the desired behaviour.
2. **Green** — write the smallest implementation that turns it green.
3. **Refactor** — clean up while keeping the tests green.

Coverage on the modules you touch must stay ≥ 90 %; the project-wide gate is
≥ 85 %.

## Updating the TODO list

`docs/TODO.md` is the single source of truth for outstanding work. When you
complete a task, mark it done with a timestamp and the commit SHA:

```
- [x] T-0042 | P3 | runtime | implement claude -p argv builder — done 2026-05-31 (sha 1a2b3c4)
```

Add new items as you discover them. The list grows to ≥ 600 entries in Phase 1.

## The prompt log

Every Claude Code session writes a `docs/prompts/NNN_phase_name.md` file with
the prompt that was issued and a one-page summary of the agent's output. Treat
it as graded evidence of the vibe-coding methodology — never delete or rewrite
history there.

## Code of conduct

Be precise, be honest, cite sources for any external code, and never silently
disable a quality gate. If a rule genuinely cannot be followed for a specific
module, document the exception as an ADR in `docs/PLAN.md`.
