# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to a simplified [Semantic Versioning](https://semver.org/)
contract: the major release is pinned to `1.00` for the duration of HW2, with
subsequent minor bumps reserved for post-grading patches.

## [Unreleased]

### Added
- _Work in progress through Phases 1–12 — see `docs/TODO.md`._

## [1.00] — 2026-05-31

### Added

- **Phase 0 (bootstrap)** — repository scaffold and directory layout; package
  skeleton `src/cosmos77_ex02/` (sdk, agents, runtime, orchestration, protocol,
  skills, tools, shared, cli); tooling (`pyproject.toml`, `uv.lock`, ruff,
  pytest with `fail_under = 85`); governance (`CLAUDE.md`, `LICENSE`,
  `CHANGELOG.md`, `CONTRIBUTING.md`, `BADGES.md`); configs (`config/setup.json`,
  `config/gatekeeper.json`, `config/logging_config.json`); quality gates
  (`scripts/check_line_cap.py`, `scripts/generate_cover_pdf.py`,
  `.pre-commit-config.yaml`, `.github/workflows/ci.yml`); core domain constants
  with tests. No business logic this phase.

### Security

- `.env.example` committed with placeholders only; the real `.env` is excluded
  via `.gitignore`. LLM authentication is the `claude` CLI subscription login —
  no API keys, tokens, or session credentials ship with the repo.
