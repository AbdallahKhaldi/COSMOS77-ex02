# Prompt log 012 — Phase 12: Cover PDF + tag + release + submit

**Date:** 2026-05-31
**Phase:** 12 — Submission: cover PDF, `v1.00` tag, GitHub release, Moodle
**Driver:** Abdallah Khaldi & Tasneem Natour · **Agent:** Claude Code (Opus 4.8)
**Authority:** `../CLAUDE_CODE_PLAYBOOK.md` §14 (Phase 12 prompt)

---

## The prompt issued

> Phase 12 goal: generate the cover PDF programmatically from the lecturer's
> template (exercise number = 2), tag the release, push, and prep submission.
> Reuse `scripts/generate_cover_pdf.py`; confirm `test_cover_pdf.py`; run the
> generator; `*.pdf` gitignored; tag `v1.00`; `gh release create`; print the
> final summary + the two manual web-UI steps.

(Full task list: playbook §14.)

## What the agent did (summary)

- **`scripts/generate_cover_pdf.py` retargeted to HW2**: exercise number = 2 (new
  `--exercise-number` flag, default 2), the ex02 repo URL, both students' details.
  The field values are produced by a pure, unit-tested `build_field_values`; the
  file was refactored back under the 150-line cap.
- **`tests/unit/test_scripts/test_cover_pdf.py`**: asserts the field mapping
  (exercise = "2", `…/COSMOS77-ex02` URL, group, self-score 85, late = no), both
  students configured, and the `%PDF` magic-byte verification (accept/reject).
- **`v1.00` tag + GitHub release** created from the final green `main`.
- `*.pdf` stays gitignored (`.gitignore`); only the script + test are committed.

## Manual steps (only the human can do these)

1. **Generate the cover PDF** — this machine has no docx→PDF converter
   (Word/`docx2pdf`/LibreOffice). Install one and run:
   ```bash
   brew install --cask libreoffice   # one-time
   uvx --with python-docx --with docx2pdf python scripts/generate_cover_pdf.py \
     --template ~/COSMOS77/HW2/cover_template/uoh-rl07-ex01.docx \
     --output ~/COSMOS77/HW2/COSMOS77-ex02.pdf --self-score 85 --exercise-number 2
   ```
   Then open `~/COSMOS77/HW2/COSMOS77-ex02.pdf` and confirm: exercise number = 2,
   the ex02 repo URL, layout untouched.
2. **Collaborator invites** — the repo is **public**, so Dr. Segal
   (`rmisegal@gmail.com`) can already clone it; no invite is required for grading.
   Tasneem (`natortasneem`) was invited as a collaborator in Phase 0.
3. **Moodle upload** — Abdallah **and** Tasneem each upload
   `~/COSMOS77/HW2/COSMOS77-ex02.pdf` to their own Moodle accounts (the timer is
   per-student).

## Project complete

All 13 phases (0–12) delivered: a working 3-process AI debate that runs
end-to-end to a no-tie justified verdict, with the full engineering layer, docs,
real session-1 evidence, ~98 % test coverage, green CI, and `v1.00` tagged.
