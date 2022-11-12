from typing import NamedTuple, List, Tuple


class Market(NamedTuple):
    id: str
    name: str
    base_currency: str
    quote_currency: str
    minimum_order_amount: Tuple[float, str]
    taker_fee: float
    maker_fee: float


class Markets(NamedTuple):
    markets: List[Market]


class Ticker(NamedTuple):
    last_price: Tuple[float, str]
    market_id: str
    max_bid: Tuple[float, str]
    min_ask: Tuple[float, str]
    price_variation_24h: float
    price_variation_7d: float
    volume: Tuple[float, str]
