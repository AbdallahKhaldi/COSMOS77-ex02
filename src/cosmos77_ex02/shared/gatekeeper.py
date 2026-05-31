"""Gatekeeper — token/USD cost meter with a hard budget cap (rule 13).

Every LLM call routes through :meth:`Gatekeeper.guard`. The gatekeeper reads
``total_cost_usd`` / ``usage`` from each ``claude -p`` JSON result (or an
``LlmResult`` object), accumulates spend, warns at ``warn_at_fraction`` of the
budget, and raises :class:`BudgetExceeded` once ``budget_usd_max`` is reached so
the debate aborts cleanly. :meth:`scrub` redacts secrets before anything is
logged (the cyber layer). Limits come from ``config/gatekeeper.json``.
"""

from __future__ import annotations

import re
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from typing import Any, TypeVar

from cosmos77_ex02.shared.logging_setup import get_logger

T = TypeVar("T")
_LOG = get_logger("cosmos77_ex02.gatekeeper")
_SECRET_RE = re.compile(
    r"(sk-[A-Za-z0-9_\-]{6,}|gh[pousr]_[A-Za-z0-9]{16,}|AKIA[0-9A-Z]{12,}"
    r"|Bearer\s+[A-Za-z0-9._\-]+|eyJ[A-Za-z0-9._\-]{10,})"
)


class BudgetExceeded(RuntimeError):
    """Raised when accumulated spend reaches the configured budget cap."""


@dataclass
class CostStats:
    """Running totals across every metered call."""

    total_cost_usd: float = 0.0
    input_tokens: int = 0
    output_tokens: int = 0
    calls: int = 0


class Gatekeeper:
    """Meters LLM cost and enforces the budget cap from ``gatekeeper.json``."""

    def __init__(self, config: Mapping[str, Any] | None = None) -> None:
        cfg = dict(config) if config is not None else self._load_default()
        self.budget_usd_max = float(cfg.get("budget_usd_max", 5.0))
        self.per_call_usd_max = float(cfg.get("per_call_usd_max", 0.5))
        self.warn_at_fraction = float(cfg.get("warn_at_fraction", 0.8))
        self.hard_stop = bool(cfg.get("hard_stop", True))
        self._stats = CostStats()
        self._warned = False

    @staticmethod
    def _load_default() -> dict[str, Any]:
        from cosmos77_ex02.shared.config import Config

        return Config().gatekeeper()

    @property
    def stats(self) -> CostStats:
        """The live cost/token counters."""
        return self._stats

    @staticmethod
    def _extract(result: Any) -> tuple[float, int, int]:
        """Pull (cost_usd, input_tokens, output_tokens) from a dict or LlmResult."""
        if isinstance(result, Mapping):
            usage = result.get("usage") or {}
            return (
                float(result.get("total_cost_usd", 0.0) or 0.0),
                int(usage.get("input_tokens", 0) or 0),
                int(usage.get("output_tokens", 0) or 0),
            )
        return (
            float(getattr(result, "cost_usd", 0.0) or 0.0),
            int(getattr(result, "input_tokens", 0) or 0),
            int(getattr(result, "output_tokens", 0) or 0),
        )

    def account(self, result: Any) -> None:
        """Record the cost/usage of one call result and warn near the cap."""
        cost, in_tok, out_tok = self._extract(result)
        if cost > self.per_call_usd_max:
            _LOG.warning("per-call cost %.4f exceeds ceiling %.4f", cost, self.per_call_usd_max)
        self._stats.total_cost_usd += cost
        self._stats.input_tokens += in_tok
        self._stats.output_tokens += out_tok
        self._stats.calls += 1
        if (
            not self._warned
            and self._stats.total_cost_usd >= self.budget_usd_max * self.warn_at_fraction
        ):
            self._warned = True
            _LOG.warning(
                "spend %.4f USD is past %.0f%% of the %.2f budget",
                self._stats.total_cost_usd,
                self.warn_at_fraction * 100,
                self.budget_usd_max,
            )

    def check_budget(self) -> None:
        """Raise :class:`BudgetExceeded` once spend reaches the cap (if hard_stop)."""
        if self.hard_stop and self._stats.total_cost_usd >= self.budget_usd_max:
            raise BudgetExceeded(
                f"spend {self._stats.total_cost_usd:.4f} USD reached cap "
                f"{self.budget_usd_max:.2f} after {self._stats.calls} calls"
            )

    def guard(self, fn: Callable[..., T], /, *args: Any, **kwargs: Any) -> T:
        """Pre-check budget, run ``fn``, account its result, post-check budget."""
        self.check_budget()
        result = fn(*args, **kwargs)
        self.account(result)
        self.check_budget()
        return result

    def cost_report(self) -> dict[str, Any]:
        """Return a serialisable summary of spend so far."""
        return {
            "total_cost_usd": round(self._stats.total_cost_usd, 6),
            "input_tokens": self._stats.input_tokens,
            "output_tokens": self._stats.output_tokens,
            "calls": self._stats.calls,
            "budget_usd_max": self.budget_usd_max,
            "remaining_usd": round(self.budget_usd_max - self._stats.total_cost_usd, 6),
        }

    @staticmethod
    def scrub(text: str) -> str:
        """Redact anything resembling an API key/token before logging."""
        return _SECRET_RE.sub("[REDACTED]", text)
