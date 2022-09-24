"""Data models."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass
class RatesRub:
    """Currency rates model."""

    czk: Decimal
    eur: Decimal
    usd: Decimal

    @classmethod
    def from_dict(cls, rates_source: dict[str, str]) -> RatesRub:
        """Make RatesRub from dict."""
        return cls(**{
            currency: Decimal(rate)
            for currency, rate in rates_source.items()
        })


@dataclass
class SummaryRates:
    """Summary rates from few sources."""

    created_at: datetime
    cash: RatesRub
    forex: RatesRub
    p2p: RatesRub
    bloomberg: RatesRub
