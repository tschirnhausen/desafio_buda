from buda import buda
from typing import List, Tuple, Optional
from api.schemas import Alert
from api.models import Alert as AlertModel
from sqlalchemy.orm import Session


class InvalidRequest(Exception):
    """ The request cannot be made because the payload has an invalid format """
    pass


def get_market_or_exception(currency: str, market: str, disable_check: bool) -> Tuple[str, str]:
    """
    Checks if the market exists and if so, returns a formatted tuple.
    If disable_check is True, then the request to get all markets won't be executed 
    """
    currency, market = currency.lower(), market.lower()

    if not disable_check:
        if f'{currency}-{market}' not in get_all_markets(): # TODO: Add cache for this method
            raise InvalidRequest('The selected market does not exist in Buda')

    return currency, market

def get_all_markets() -> List[str]:
    """
    Get the available markets at Buda

    This function simply calls the Buda SDK and returns the available markets as a list of strings, with the format:
    {currency}-{market}. Where "currency" is the traded asset and "market" is the exchange currency.

    Example:
    ['btc-clp', 'btc-cop', 'eth-clp', 'eth-btc' ...]
    """
    return [market.name for market in buda.Buda().get_markets().markets]

def get_market_spread(currency: str, market: str, disable_check: bool = False):
    """
    Obtains the buying and selling prices of a currency in a market, if exists.

    This function simply calls the Buda SDK to get the ticker of a market and returns a dictionary with the bid and ask prices.
    """

    currency, market = get_market_or_exception(currency, market, disable_check)

    market_ticker: buda.schemas.Ticker = buda.Buda().get_ticker(currency=currency, market=market)

    return {
        'bid': market_ticker.max_bid[0],
        'ask': market_ticker.min_ask[0],
        'spread': round(
            market_ticker.min_ask[0] - market_ticker.max_bid[0],
            2
        ),
        'market': f'{currency}-{market}'
    }

def get_all_markets_spread() -> List[dict]:
    """
    Get the latest asks and bids from all the markets in Buda.

    Since the markets to be queried are obtained directly from the API, the check to see if it is a valid market is omitted.
    """
    available_markets: List[str] = [market.split('-') for market in get_all_markets()]

    return [
        get_market_spread(
            currency=market_data[0],
            market=market_data[1],
            disable_check=True
        ) for market_data in available_markets
    ]

def create_alert(db: Session, alert: Alert) -> Optional[AlertModel]:
    db_alert = AlertModel(
        type=alert.type,
        market=alert.market,
        spread=alert.spread
    )
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    return db_alert

def get_alert(db: Session, alert_id: int) -> Optional[AlertModel]:
    return db.query(AlertModel).filter(AlertModel.id == alert_id).first()