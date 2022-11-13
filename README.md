# Desafío Buda
![Passed Tests](https://img.shields.io/badge/tests-18%20passed%2C%200%20failed-brightgreen) ![version](https://img.shields.io/badge/version-1.0.0-blue)

Solution developed in Python3.8 by the applicant Javier Valenzuela for the Buda challenge.
The instructions of the solved problem correspond to [Task 1](https://budapuntocom.notion.site/Spread-API-2fb7f25ef5344d3081c48259da05ae94).

## Setup

### Requirements
1. Python 3.8.10
2. Pip
3. Pipenv
4. requests 2.28.1
5. pytest 7.2.0
6. fastapi
7. uvicorn

### Running tests
Tests are located at `tests` folder. Regular usage should be `pytest tests/<test_filename>.py --log-cli-level=10`.

### Starting the raw app
1. First create a virtual environment, activate it and install the requirements using `pipenv`
`pipenv shell`
`pipenv install`
2. In the main directory, run the following command for run the application
`uvicorn main:app --reload`
3. Server is running when you see `Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)` on your console

## Documentation

### UI Documentation by Swagger UI
Once the server is running, you can access to the interactive API documentation provided by Swagger UI, by accessing to: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs). You will be able to see the schemas, exceptions, docstrings and parameters types, even try the API without any usage of `Postman` or `curl`.

### Raw `curl` documentation

#### Get spread for a market

##### Request

`GET /spread/{currency}/{market}/`

    curl -X 'GET' 'http://127.0.0.1:8000/spread/btc/clp/' -H 'accept: application/json'

| Path parameter | Required    | Description    | Type    | Allowed values    |
| :---:   | :---: | :---: | :---: | :---: |
| currency | yes   | Currency in exchange   | string | **btc**, **eth**, **ltc**, **bch**, **usdc** |
| market | yes   | Market of exchange   | string | **clp**, **pen**, **cop**, **usdc** |

##### Body
No parameters required

#### Response

    HTTP/1.1 200 OK
    Date: Thu, 13 Nov 2022 15:30:30 GMT
    Status: 200 OK
    Connection: close
    Content-Type: application/json
    Content-Length: 73

    {
        "spread": "26315.0",
        "market": "btc-clp"
    }

#### Get spreads for all available markets

##### Request

`GET /spreads/`

    curl -X 'GET' 'http://127.0.0.1:8000/spreads/' -H 'accept: application/json'

##### Body
No parameters required

#### Response

    HTTP/1.1 200 OK
    Date: Thu, 13 Nov 2022 15:30:30 GMT
    Status: 200 OK
    Connection: close
    Content-Type: application/json
    Content-Length: 1601

    [
        {
            "bid": 14873120,
            "ask": 14896315,
            "spread": 23195,
            "market": "btc-clp"
        },
        {
            "bid": 77000005.01,
            "ask": 79322314.17,
            "spread": 2322309.16,
            "market": "btc-cop"
        },
        ...
        {
            "bid": 16500.01,
            "ask": 16682.3724,
            "spread": 182.36,
            "market": "btc-usdc"
        }
    ]

#### Create an alert for a market

##### Request

`POST /alert/`

    curl -X 'POST' 'http://127.0.0.1:8000/alert/' -H 'accept: application/json' -H 'Content-Type: application/json' -d '{"type": "above","currency": "btc", "market": "clp", "spread": 500000}'

##### Body
| Parameter | Required    | Description    | Type    | Allowed values    |
| :---:   | :---: | :---: | :---: | :---: |
| type | yes   | Select if alert should display a fulfill value when spread is above or under a threshold   | string | **above**, **under** |
| currency | yes   | Currency in exchange   | string | **btc**, **eth**, **ltc**, **bch**, **usdc** |
| market | yes   | Market of exchange   | string | **clp**, **pen**, **cop**, **usdc** |
| spread | yes   | Threshold for change the status of the alert   | float | - |


#### Response

    HTTP/1.1 200 OK
    Date: Thu, 13 Nov 2022 15:30:30 GMT
    Status: 200 OK
    Connection: close
    Content-Type: application/json
    Content-Length: 33

    {
        "status": "created",
        "alert_id": 1
    }

#### Check the current status of the created alert

`GET /alert/{alert_id}/`

    curl -X 'GET' 'http://127.0.0.1:8000/alert/1/' -H 'accept: application/json'

#### Response

    HTTP/1.1 200 OK
    Date: Thu, 13 Nov 2022 15:30:30 GMT
    Status: 200 OK
    Connection: close
    Content-Type: application/json
    Content-Length: 101

    {
        "alert_data": {
            "id": 1,
            "market": "btc-clp",
            "target_spread": 500000,
            "type": "above"
        },
        "status": "pending"
    }


| Parameter    | Description    | Type    | Possible values    |
| :---:   | :---: | :---: | :---: |
| status | Indicates whether a threshold has already been reached for a market spread.   | string | **pending**, **fulfill** |
| alert_data | Summary of the alert   | dict | - |
