# PRD — JSON IPC protocol

> **Placeholder — filled in Phase 1.** See `../../CLAUDE_CODE_PLAYBOOK.md` §3 for the full prompt.

The pydantic message envelope {msg_id, ts, sender, recipient, role, ping_no, turn_type, content, citations[], word_count, tokens, cost_usd}; validation rules; rejection/retry on missing citation or over-length; child→judge→child routing.
