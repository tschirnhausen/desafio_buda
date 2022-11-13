import pytest
import api.services as services
from buda import buda

def test_get_market_or_exception_format():
    """
    Tests that the service returns lowercase strings when receiving a mixture of uppercase and lowercase letters.
    """
    currency, market = services.get_market_or_exception(
        currency='BTC',
        market='cLp',
        disable_check=True
    )

    assert currency, market == ['btc', 'clp']

def test_get_market_or_exception_market_validation():
    """
    Tests that the service detects a market belonging to the list of valid markets.
    """
    currency, market = services.get_market_or_exception(
        currency='eth',
        market='clp',
        disable_check=False
    )

    assert currency, market == ['eth', 'clp']

def test_get_market_or_exception_market_validation_exception():
    """
    Tests that the service detects an invalid market.
    """
    with pytest.raises(services.InvalidRequest):
        currency, market = services.get_market_or_exception(
            currency='eth',
            market='invalid',
            disable_check=False
        )

def test_get_markets():
    """
    Tests that the service is collecting a list with the markets names
    """
    markets_names: list = services.get_all_markets()
    assert len(markets_names) > 0

def test_get_market_spread():
    """
    Tests that spread actually exists and is calculated well.
    As the notes says that bid can be greater than ask for a few moments, this test does not check if
    spread is a positive number
    """
    market_ticker: dict = services.get_market_spread(
        currency='btc',
        market='clp'
    )

    bid: float = market_ticker.get('bid')
    ask: float = market_ticker.get('ask')
    spread: float = market_ticker.get('spread')

    assert bid > 0 and ask > 0 and spread == round(ask-bid, 2)

def test_get_market_spread_without_validation():
    """
    Tests that an BudaInvalidResponse Exception is raised when disable check is forced and 
    an invalid market is passed
    """
    with pytest.raises(buda.exceptions.BudaInvalidResponse):
        market_ticker: dict = services.get_market_spread(
            currency='btc',
            market='invalid',
            disable_check=True
        )

def test_get_all_markets_spread():
    """
    Tests that the service is returing a list with the market required data
    """
    markets_data: list = services.get_all_markets_spread()
    assert len(markets_data) > 0 
