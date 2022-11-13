from typing import NamedTuple, List, Tuple


class Market(NamedTuple):
    """
        Attribute            | Type               | Description

        id	                 | [string]	          | Market identifier
        name	             | [string]	          | Name of the market which corresponds to the market_id
        base_currency	     | [string]	          | Currency of exchange
        quote_currency	     | [string]	          | Currency of payment
        minimum_order_amount | [amount, currency] | Minimum order size accepted
        taker_fee	         | [amount]	          | Fee paid for a taker order
        maker_fee	         | [amount]	          | Fee paid for a maker order

    """
    id: str
    name: str
    base_currency: str
    quote_currency: str
    minimum_order_amount: Tuple[float, str]
    taker_fee: float
    maker_fee: float


class Markets(NamedTuple):
    """
        Attribute  | Type     | Description

        markets    | [Market] | List of Market schemas
    """
    markets: List[Market]


class Ticker(NamedTuple):
    """       
        Attribute           |  Type    | Description

        last_price          | [float]  | Last price of the currency in the current market
        market_id           | [string] | Market name with format {currency}-{market} 
        max_bid             | [float]  | Current maximum bid in the market
        min_ask             | [float]  | Current minimum ask in the market
        price_variation_24h | [float]  | Percentage of variation in the period)
        price_variation_7d  | [float]  | Percentage of variation in the period
    """
    last_price: Tuple[float, str]
    market_id: str
    max_bid: Tuple[float, str]
    min_ask: Tuple[float, str]
    price_variation_24h: float
    price_variation_7d: float
    volume: Tuple[float, str]
