"""The cover-PDF generator: field mapping (exercise 2, ex02 URL) + PDF check.

Loads the standalone script by path (scripts/ is not a package) and tests the
pure field-builder + the %PDF verification — no python-docx or converter needed.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

_SCRIPT = Path(__file__).resolve().parents[3] / "scripts" / "generate_cover_pdf.py"
_spec = importlib.util.spec_from_file_location("generate_cover_pdf", _SCRIPT)
gcp = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(gcp)  # type: ignore[union-attr]


def _fields() -> dict[str, str]:
    return dict(gcp.build_field_values(2, 85))


def test_exercise_number_is_two() -> None:
    assert _fields()["Submitting an exercise number"] == "2"


def test_repo_url_is_ex02() -> None:
    assert _fields()["Link to GITHUB"].endswith("COSMOS77-ex02")


def test_group_self_score_and_late_flag() -> None:
    fields = _fields()
    assert fields["Group ID code"] == "COSMOS77"
    assert fields["Recommendation for self-scoring"] == "85"
    assert fields["A late submission confirmation"] == "no"


def test_both_students_configured() -> None:
    headers = [h for h, _ in gcp._STUDENTS]
    ids = [vals[0] for _, vals in gcp._STUDENTS]
    assert headers == ["Student 1", "Student 2"]
    assert ids == ["212389712", "323118794"]


def test_verify_pdf_accepts_magic_bytes(tmp_path: Path) -> None:
    pdf = tmp_path / "cover.pdf"
    pdf.write_bytes(b"%PDF-1.7\n...content...")
    gcp.verify_pdf(pdf)  # must not raise


def test_verify_pdf_rejects_non_pdf(tmp_path: Path) -> None:
    bad = tmp_path / "cover.pdf"
    bad.write_bytes(b"not a pdf at all")
    with pytest.raises(RuntimeError, match="not a valid PDF"):
        gcp.verify_pdf(bad)
