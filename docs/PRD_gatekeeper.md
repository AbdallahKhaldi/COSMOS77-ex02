# PRD — Gatekeeper (token economy)

> **Placeholder — filled in Phase 1.** See `../../CLAUDE_CODE_PLAYBOOK.md` §3 for the full prompt.

Every agent call passes through it; reads total_cost_usd/usage from the claude -p JSON, accumulates spend, warns at warn_at_fraction, hard-stops cleanly at budget_usd_max, and scrubs secrets from logs.
