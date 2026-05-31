"""Shared pytest fixtures and configuration for the COSMOS77-ex02 suite.

Phase 0 establishes the harness; reusable fixtures (a mock ``claude -p``
runtime, fake LLM JSON results, temp config/log dirs) are added in later
phases. A hard invariant for this whole directory: no fixture or test ever
invokes the real ``claude`` binary or any network — all such I/O is mocked
(CLAUDE.md rule 6, acceptance A9). Live end-to-end checks are marked ``live``
and excluded from CI.
"""

from __future__ import annotations
