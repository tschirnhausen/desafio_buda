from . import sdk
from . import schemas, exceptions, constants
from typing import Iterable
from decimal import Decimal


class Buda(sdk.BaseSDK):
    '''
        Main Buda SDK class
        Implement the endpoints required for the challenge.

        Usage for public API: Buda().get_data()
        Note: This challenge doesn't require the private keys

    '''

    NAME: str = 'BUDA'
    VERSION: int = 2
    PRODUCTION_BASE_URL: str = 'https://www.buda.com/api/v2/'
    SANDBOX_BASE_URL: str = 'https://www.buda.com/api/v2/'

    def __init__(
        self,
        api_key: str = None,
        api_secret: str = None,
        sandbox: bool = False,
        debug: bool = False
    ):
        super().__init__(sandbox, debug)

        self.api_key = api_key
        self.api_secret = api_secret

    def buda_endpoint(
        self,
        method: str,
        url: str,
        auth: dict = None,
        data: dict = None,
        optional_data: dict = None,
        query_params: dict = None,
        success_codes: Iterable = None
    ) -> dict:
        ''' Generic Buda endpoint '''

        return self.json_endpoint(
            method=method,
            url=url,
            data=data,
            auth=auth,
            optional_data=optional_data,
            query_params=query_params,
            success_codes=success_codes,
            error_exc=exceptions.BudaServicesException
        )

    
    def get_markets(self) -> schemas.Markets:
        markets_data: dict = self.buda_endpoint(
            method='get',
            url='markets'
        )

        if constants.ResponseErrors.is_error(markets_data.get('code')):
            raise exceptions.BudaInvalidResponse(f'Invalid response from Buda: {markets_data.get("message")}')

        total_markets: list = markets_data.get('markets')

        return schemas.Markets(
            markets=[
                schemas.Market(
                    id=market.get('id'),
                    name=market.get('name'),
                    base_currency=market.get('base_currency'),
                    quote_currency=market.get('quote_currency'),
                    minimum_order_amount=[
                        market.get('minimum_order_amount')[0],
                        market.get('minimum_order_amount')[1]
                    ],
                    taker_fee=market.get('taker_fee'),
                    maker_fee=market.get('maker_fee')
                ) for market in total_markets
            ] 
        )



    def get_ticker(self, currency: str, market: str) -> schemas.Ticker:
        ticker_data: dict = self.buda_endpoint(
            method='get',
            url=f'markets/{currency}-{market}/ticker'
        )
        
        if constants.ResponseErrors.is_error(ticker_data.get('code')):
            raise exceptions.BudaInvalidResponse(f'Invalid response from Buda: {ticker_data.get("message")}')

        unpacked_ticker: dict = ticker_data.get('ticker')


        return schemas.Ticker(
            last_price=[
                float(unpacked_ticker.get('last_price')[0]),
                unpacked_ticker.get('last_price')[1]
            ],
            market_id=unpacked_ticker.get('market_id'),
            max_bid=[
                float(unpacked_ticker.get('max_bid')[0]),
                unpacked_ticker.get('max_bid')[1]
            ],
            min_ask=[
                float(unpacked_ticker.get('min_ask')[0]),
                unpacked_ticker.get('min_ask')[1]
            ],
            price_variation_24h=unpacked_ticker.get('price_variation_24h'),
            price_variation_7d=unpacked_ticker.get('price_variation_7d'),
            volume=[
                float(unpacked_ticker.get('volume')[0]),
                unpacked_ticker.get('volume')[1]
            ],
        ) 
