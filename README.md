# COSMOS77-ex02 — AI Agent Debate (UOH-RL07 HW2)

> **Placeholder.** The full lab report — abstract, architecture diagrams, the
> complete session-1 JSON dialogue, the judged verdict, cost analysis, and the
> self-assessment — is generated in **Phase 10**. This file exists so the
> package builds and the repo has a front page during Phases 0–9.

**Authors:** Abdallah Khaldi (212389712) · Tasneem Natour (323118794)
**Course:** UOH-RL07 — Vibe Coding & AI Agents (Dr. Yoram Segal) · Semester 2026

## What this will be

Three real OS processes — a **Judge** (father), a **Pro** debater, and a **Con**
debater — argue *"Is social media a net positive for society?"* over ≥10 pings
per side. Every message is JSON, routed child → judge → child; each debater must
cite a web source every turn; the judge declares a justified winner with **no
tie**. The system is driven entirely by the `claude` CLI (`claude -p`), metered
by a token/USD **Gatekeeper**, supervised by a **Watchdog**, and operated from a
terminal menu over a single **SDK**.

## Quickstart (preview)

```bash
# Prerequisites: uv, and the `claude` CLI logged in on a Max/Pro subscription
# (NO API key needed). See CLAUDE.md and docs/ for the binding rules.
uv sync
uv run cosmos77-debate menu     # available from Phase 8
```

## Project status

Built phase-by-phase per [`../CLAUDE_CODE_PLAYBOOK.md`](../CLAUDE_CODE_PLAYBOOK.md).
See [`docs/TODO.md`](docs/TODO.md) for task tracking, [`docs/prompts/`](docs/prompts/)
for the graded vibe-coding prompt log, and [`CHANGELOG.md`](CHANGELOG.md) for the
release history. License: [MIT](LICENSE).

## Acknowledgements

This project is **vibe-coded with [Claude Code](https://claude.com/claude-code)**
(Anthropic's Claude Opus 4.8), driven phase-by-phase by the two student authors per
the UOH-RL07 methodology. Every prompt issued to the agent and a summary of its work
is logged under [`docs/prompts/`](docs/prompts/) as graded evidence of the workflow;
the full *"How we used AI agents"* write-up lands in the Phase 10 README.
