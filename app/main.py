from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import api.services as services
from api.schemas import Alert
from api.models import Base
from database import engine
from utils import get_db


Base.metadata.create_all(bind=engine)
app = FastAPI()

@app.get(
    '/spread/{currency}/{market}/',
    summary='Get spread for a specified market at Buda'
)
def get_spread_data(currency: str, market: str):
    try:
        ticker_data: dict = services.get_market_spread(currency=currency, market=market)
    except services.InvalidRequest:
        raise HTTPException(
            status_code=400,
            detail='Market does not exist'
        )
    
    return {
        'spread': ticker_data.get("spread"),
        'market': ticker_data.get("market")
    }


@app.get(
    '/spreads/',
    summary='Get spreads for all available markets at Buda'
)
def get_all_spreads():
    try:
        return services.get_all_markets_spread()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail='Internal error'
        )


@app.post(
    '/alert/',
    summary='Creates an alert for checking the spread of a market'
)
def create_alert(alert: Alert, db: Session = Depends(get_db)):
    """
    Create an alert with all the information:

    - **type**: select for checking a spread **under** or **above** a desired value
    - **currency**: currency of market, i.e. **btc**, **eth**, **usdc**, **ltc**
    - **market**: market for the selected currency, i.e. **clp**, **pen**, **cop**
    - **spread**: positive value for the spread
    """
    try:
        create_alert = services.create_alert(db=db, alert=alert)
        return {
            'status': 'created',
            'alert_id': create_alert.id
        }
    except services.InvalidRequest as e:
        raise HTTPException(
            status_code=400,
            detail='Error when creating alert. Be sure that the market exists or use the correct type for the other parameters'
        )


@app.get(
    '/alert/{alert_id}/',
    summary='Get alert information'
)
def get_alert_data(alert_id: int, db: Session = Depends(get_db)):
    """
    Get alert data information

    - **alert_data**: Summary of the requested alert
    - **status**: Tells you if the spread is above or under the alert threshold. 
        - Possible values: 
            - fulfill: The condition was fulfilled
            - pending: The condition is not currently being met.
    """
    try:
        return services.get_alert(db=db, alert_id=alert_id)
    except services.InvalidRequest:
        raise HTTPException(
            status_code=404,
            detail=f'Alert with id {alert_id} not found'
        )
