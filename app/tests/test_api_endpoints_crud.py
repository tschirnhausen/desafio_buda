import pytest

from fastapi.testclient import TestClient
from api.schemas import Alert
from main import app

client = TestClient(app)

@pytest.fixture
def get_valid_currency() -> str:
    return 'btc'

@pytest.fixture
def get_invalid_currency() -> str:
    return 'cat'

@pytest.fixture
def get_valid_market() -> str:
    return 'clp'

@pytest.fixture
def get_invalid_market() -> str:
    return 'dog'

@pytest.fixture
def get_invalid_index() -> int:
    return -1

@pytest.fixture
def get_valid_above_alert(get_valid_currency, get_valid_market) -> Alert:
    return Alert(
        type='above',
        currency=get_valid_currency,
        market=get_valid_market,
        spread=50000
    ).dict()

@pytest.fixture
def get_valid_under_alert(get_valid_currency, get_valid_market) -> Alert:
    return Alert(
        type='under',
        currency=get_valid_currency,
        market=get_valid_market,
        spread=50000
    ).dict()

@pytest.fixture
def get_invalid_alert(get_invalid_currency, get_invalid_market) -> Alert:
    return Alert(
        type='above',
        currency=get_invalid_currency,
        market=get_invalid_market,
        spread=20000
    ).dict()

def test_single_market_spread(get_valid_currency, get_valid_market):
    """
    Tests if API returns an actual spread for an existent market
    """
    response = client.get(f'/spread/{get_valid_currency}/{get_valid_market}/')
    assert response.status_code == 200

def test_single_market_spread_invalid(get_valid_currency, get_invalid_market):
    """
    Tests if API raises an error when an actual spread is requested for an inexistent market
    """
    response = client.get(f'/spread/{get_valid_currency}/{get_invalid_market}/')
    assert response.status_code == 400

def test_single_market_spread_method(get_valid_currency, get_valid_market):
    """
    Tests if another method returns the correct error
    """
    response = client.post(f'/spread/{get_valid_currency}/{get_valid_market}/')
    assert response.status_code == 405

def test_get_all_markets():
    """
    Tests if API returns a list with markets when receives a request
    """
    response = client.get('/spreads/')
    assert response.status_code == 200 and len(response.json()) > 0

# Crud tests
def test_create_valid_alert(get_valid_above_alert):
    """
    Tests if API adds a valid alert to DB
    """
    response = client.post(
        '/alert/',
        json=get_valid_above_alert
    )
    assert response.status_code == 200 and response.json().get('alert_id') > 0

def test_create_invalid_alert(get_invalid_alert):
    """
    Tests if API detects an invalid schema and returns an error
    """
    response = client.post(
        '/alert/',
        json=get_invalid_alert
    )
    assert response.status_code == 400

def test_get_valid_alert(get_valid_under_alert):
    """
    Tests if API returns an existent and recent created alert
    """
    create_alert = client.post(
        '/alert/',
        json=get_valid_under_alert
    )
    created_alert_id: int = create_alert.json().get('alert_id')

    response = client.get(
        f'/alert/{created_alert_id}/'
    )

    assert response.status_code == 200 and response.json().get('alert_data').get('id') == created_alert_id
    
def test_get_invalid_alert(get_invalid_index):
    """
    Tests if API detects an invalid alert id an return a 404 status
    """
    response = client.get(f'/alert/{get_invalid_index}')

    assert response.status_code == 404
