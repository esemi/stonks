"""P2P exchange chats rates calculations."""
from decimal import Decimal

from app import currency
from app.rates_model import RatesRub
from app.settings import app_settings


def get_rates(cash_rates: RatesRub, forex_rates: RatesRub) -> RatesRub:
    """Return p2p currency exchange rates."""
    rates: dict[str, Decimal] = {}
    for currency_code in app_settings.supported_foreign_currencies:
        rate_with_discount = round(getattr(cash_rates, currency_code) - app_settings.p2p_rate_discount)
        rates[currency_code] = Decimal(max(rate_with_discount, getattr(forex_rates, currency_code)))

    rates[currency.CZK] = Decimal(0)  # никто не торгует кроной в глобальных p2p-чатах

    return RatesRub(**rates)
