"""Pin the project version and the config-version validation contract."""

from __future__ import annotations

import pytest

from cosmos77_ex02.shared import version


def test_version_constant_is_one_dot_zero_zero() -> None:
    assert version.VERSION == "1.00"


def test_validate_config_version_accepts_match() -> None:
    version.validate_config_version("1.00")  # must not raise


def test_validate_config_version_rejects_mismatch() -> None:
    with pytest.raises(ValueError, match="version"):
        version.validate_config_version("0.99")


def test_validate_config_version_rejects_empty_string() -> None:
    with pytest.raises(ValueError, match="version"):
        version.validate_config_version("")


def test_package_exposes_dunder_version() -> None:
    import cosmos77_ex02

    assert cosmos77_ex02.__version__ == "1.00"
