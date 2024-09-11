"""Data models."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass
class RatesRub:
    """Provider rates."""

    czk: Decimal
    eur: Decimal
    usd: Decimal
    cny: Decimal

    @classmethod
    def from_dict(cls, rates_source: dict[str, str]) -> RatesRub:
        """Make RatesRub from dict."""
        return cls(**{
            currency: Decimal(rate)
            for currency, rate in rates_source.items()
        })


@dataclass
class CurrencyRates:
    """Currency rates."""

    currency: str
    cash: Decimal
    forex: Decimal
    p2p: Decimal
    moex: Decimal

    @property
    def avg(self) -> Decimal:
        """Average rate between FX and cash."""
        return (self.cash + self.forex) / Decimal(2)


@dataclass
class SummaryRates:
    """Summary rates by provider."""

    created_at: datetime
    cash: RatesRub
    forex: RatesRub
    p2p: RatesRub
    moex: RatesRub

    def get_rates(self, currency_code: str) -> CurrencyRates:
        """Get rates for selected currency."""
        return CurrencyRates(
            currency=currency_code,
            cash=getattr(self.cash, currency_code),
            forex=getattr(self.forex, currency_code),
            p2p=getattr(self.p2p, currency_code),
            moex=getattr(self.moex, currency_code),
        )
