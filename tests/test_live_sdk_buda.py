import pytest
from buda import buda
from typing import Optional

@pytest.fixture
def buda_instance() -> buda.Buda:
    ''' Returns an instance of Buda environment '''
    return buda.Buda()

def test_get_markets(buda_instance) -> bool:
    markets_data: Optional[list] = buda_instance.get_markets().markets
    assert type(markets_data) is list and len(markets_data) > 0

def test_get_ticker(buda_instance) -> bool:
    currency: str = 'btc'
    market: str = 'clp'

    market_data: Optional[buda.schemas.Ticker] = buda_instance.get_ticker(
        currency=currency,
        market=market
    )

    assert type(market_data) == buda.schemas.Ticker and market_data.market_id.lower() == f'{currency}-{market}'

