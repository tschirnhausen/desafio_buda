from fastapi import FastAPI, Depends
from api import models, schemas
from sqlalchemy.orm import Session
from database import SessionLocal, engine

import services

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get(
    '/spread/{currency}/{market}/',
    summary='Get spread for a specified market at Buda'
)
async def get_spread_data(currency: str, market: str):
    try:
        ticker_data: dict = services.get_market_spread(currency=currency, market=market)
    except services.InvalidRequest:
        return {
            'error': 'market does not exist'
        }
    
    return {
        'spread': f'${ticker_data.get("spread")} {ticker_data.get("market").upper()}',
        'market': ticker_data.get("market")
    }

@app.get(
    '/spreads/',
    summary='Get spreads for all available markets at Buda'
)
async def get_all_spreads():
    try:
        return services.get_all_markets_spread()
    except Exception as e:
        return {
            'error': 'server error',
            'detail': e
        }

@app.post(
    '/alert/',
    summary='Creates an alert for checking the spred of a market'
)
async def create_alert(alert: schemas.Alert, db: Session = Depends(get_db)):
    """
    Create an alert with all the information:

    - **type**: select for checking a spread under or above a desired value
    - **market**: market with format: {currency}-{market}. i.e. btc-clp
    - **spread**: value for the spread
    """
    try:
        create_alert = services.create_alert(db=db, alert=alert)
        return {
            'status': 'created',
            'alert_id': create_alert.id
        }
    except Exception as e:
        return {
                    'error': 'server error',
                    'detail': e
                }

@app.get(
    '/alert/{alert_id}/',
    summary='Get alert information'
)
async def get_alert_data(alert_id: int, db: Session = Depends(get_db)):
    """
    Get alert data information
    """
    try:
        alert = services.get_alert(db=db, alert_id=alert_id)
        return {
            'alert_id': alert.id,
            'alert_market': alert.market,
            'alert_spread': alert.spread,
            'type': alert.type
        }
    except Exception as e:
        return {
                    'error': 'server error',
                    'detail': e
                }