"""Data models."""

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass
class RatesRub:
    """Currency rates model."""

    czk: Decimal
    eur: Decimal
    usd: Decimal


@dataclass
class SummaryRates:
    """Summary rates from few sources."""

    created_at: datetime
    cash: RatesRub
    forex: RatesRub
