# CLAUDE.md — Project rules of engagement (binding for every prompt)

This repo is HW2 (AI Agent Debate) for Dr. Yoram Segal's UOH-RL07 course.
Every prompt I send in this repo inherits these rules. Violating any rule
fails an automated check. HW2-specific acceptance criteria (A1–A15) are in
../CLAUDE_CODE_PLAYBOOK.md §1.5 — also binding.

## The 17 rules
1. 150-line hard cap per .py file (blank lines + comments included). Split it.
2. SDK architecture: all business logic via class SDK in src/cosmos77_ex02/sdk/sdk.py.
   CLI/menu/orchestrator/external callers use only the SDK.
3. OOP, no duplication. 2 files → shared module; 3 files → base class/mixin.
4. Zero hardcoded config (topic, pings, timeouts, budget, paths) → config/*.json or .env.
5. uv is the only package manager. Never pip / venv / python script.py.
6. TDD red→green→refactor. Mock ALL subprocess/LLM/network I/O; no live calls in tests.
7. Coverage ≥ 85%.
8. ruff check returns zero violations.
9. No secrets in repo. .env.example placeholders only (LLM auth is the claude CLI login).
10. Versioning starts at 1.00 (version.py, every config, git tag v1.00).
11. Conventional Commits per task; reference TODO IDs.
12. Prompt log: every session → docs/prompts/NNN_*.md.
13. Gatekeeper: every agent/LLM call routes through shared/gatekeeper.py; meters
    token/USD cost and hard-stops at the config budget cap.
14. CLI only (Claude Code in the terminal). The DELIVERABLE is a Python program
    that runs the agents — never a hand-typed chat debate.
15. Docstrings on every public class/function/module (why, not what).
16. Type hints on every public signature. No bare Any.
17. Deterministic tests. Seed random/numpy. No flakes.

## English only
All code, comments, docs, skills, and debate output are in English (Arabic is forbidden by the spec).

## When in doubt
Pick less code, fewer deps, clearer docstrings. If a rule is impossible for a
module, write an ADR in docs/PLAN.md — never silently violate.
