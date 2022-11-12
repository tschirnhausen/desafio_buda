import pytest
import services
from typing import Tuple
from buda import buda

def test_get_market_or_exception_format():
    currency, market = services.get_market_or_exception(
        currency='BTC',
        market='cLp',
        disable_check=True
    )

    assert currency, market == ['btc', 'clp']

def test_get_market_or_exception_market_validation():
    currency, market = services.get_market_or_exception(
        currency='eth',
        market='clp',
        disable_check=False
    )

    assert currency, market == ['eth', 'clp']

def test_get_market_or_exception_market_validation_exception():
    with pytest.raises(services.InvalidRequest):
        currency, market = services.get_market_or_exception(
            currency='eth',
            market='invalid',
            disable_check=False
        )

def test_get_markets():
    markets_names: list = services.get_all_markets()
    assert len(markets_names) > 0

def test_get_market_spread():
    market_ticker: dict = services.get_market_spread(
        currency='btc',
        market='clp'
    )

    assert market_ticker.get('bid') > 0 and market_ticker.get('ask') > 0 and type(market_ticker.get('spread')) is float

def test_get_market_spread_without_validation():
    with pytest.raises(buda.exceptions.BudaInvalidResponse):
        market_ticker: dict = services.get_market_spread(
            currency='btc',
            market='invalid',
            disable_check=True
        )

def test_get_all_markets_spread():
    markets_data: list = services.get_all_markets_spread()
    assert len(markets_data) > 0
