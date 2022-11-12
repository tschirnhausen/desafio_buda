import json
import requests
import hmac
import hashlib
import base64
import logging

from typing import Iterable

from Crypto.Cipher import AES

app_logger = logging.getLogger('app')


class UnsupportedMethodError(Exception):
    '''
        Method not supported or not implemented
    '''
    pass


class UnknownSchemaError(Exception):
    '''
        Received an unknown schema.
        The exception string contains the error details.
    '''
    pass


class BaseSDK:
    '''
        The base class for SDK's. Implements basic common SDK initialization
        and basic utility methods.

        Inherit from this class to implement a new SDK. You must set NAME,
        PRODUCTION_BASE_URL and SANDBOX_PRODUCTION_URL in the class definition,
        otherwise an exception will be raised when an instance is created.

        if debug is activated, requests full verbose will be logged.
    '''

    NAME = 'Empty SDK'
    VERSION = '1.0.0'
    PRODUCTION_BASE_URL = ''
    SANDBOX_BASE_URL = ''
    DEFAULT_TIMEOUT = 15

    def __init__(
        self,
        sandbox: bool = False,
        debug: bool = False,
        global_timeout: int = DEFAULT_TIMEOUT,
    ):
        if self.NAME == 'Empty SDK':
            raise Exception('Please set a name for your SDK.')
        if self.PRODUCTION_BASE_URL == '':
            raise Exception('Please set a production url for your SDK.')
        if self.SANDBOX_BASE_URL == '':
            raise Exception('Please set a sandbox url for your SDK.')
        
        self._last_response = None
        
        self._rest_session = requests.Session()
        self._base_url = self.SANDBOX_BASE_URL if sandbox else self.PRODUCTION_BASE_URL
        self._debug = debug
        self._default_timeout = global_timeout

        self._rest_session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': f'{self.NAME} Python SDK v{self.VERSION}',
        })

    @staticmethod
    def insert_optional_dict(
        target: dict, 
        optionals: dict, 
        discard_value=None
    ) -> bool:
        '''
            Inserts all keys that have a value != discard_value from optionals 
            to target dict.

            Returns True if the target dict was updated, False otherwise.
        '''
        l = len(target)
        for key, value in optionals.items():
            if value is not None:
                target[key] = value
        
        if l != len(target):
            return True
        return False

    
    @staticmethod
    def response_validate_json(response: requests.Response):
        '''
            Validates the response schema by raising the appropiate generic exception
            if the response cant be parsed to json. If the response is OK, returns the
            ready to use data as dict.
        '''
        try:
            data = response.json()
        except ValueError:
            raise UnknownSchemaError(
                f'The received data is an unknown schema: {response.text}'
            )
        return data
    
    def set_debug(self, enabled: bool):
        self._debug = enabled

    def json_endpoint(
        self,
        method: str,
        url: str,
        headers: dict = None,
        data: dict = None,
        optional_data: dict = None,
        query_params: dict = None,
        auth=None,
        success_codes: Iterable[int] = None,
        error_exc: Exception = Exception,
        force_url: str = None,
        form: dict = None,
        status_code_key: str = None,
        timeout: int = None,
    ) -> dict:
        '''
            The generic procedure of any json request.
            If success_codes is None, any code will be accepted. If not, if the returned
            status code is not any of success_codes, exc will be raised.

            If status_code_key is not None, the status code will be added to the result data
            assigned to the provided key. Be careful with overriding some existing key in the
            response data. Useful when multiple status codes are expected.

            Returns None if response body is empty.
        '''
        self._last_response = None
        
        _raw_request_data = {
            'url': url,
            'auth': auth,
        }

        if data is not None:
            if optional_data is not None:
                BaseSDK.insert_optional_dict(
                    data,
                    optional_data,
                )
            _raw_request_data['data'] = data
        if headers is not None:
            _raw_request_data['headers'] = headers
        if query_params is not None:
            _raw_request_data['params'] = query_params
        if form is not None:
            _raw_request_data['files'] = query_params
        
        _request_data = self.process_request_args(_raw_request_data)

        if force_url is not None:
            _request_data['url'] = force_url

        _request_data['timeout'] = self._default_timeout if timeout is None else timeout
        
        if self._debug:
            app_logger.debug(
                f'''
                    -- Request from {self.NAME} --
                    URL: {_request_data.get('url')}
                    Query params: {_request_data.get('params')}
                    Method: {method}
                    Headers: {_request_data.get('headers')}
                    Data: {_request_data.get('data')}
                    Form-data: {_request_data.get('form')}
                '''
            )

        if method == 'get':
            response = self._rest_session.get(
                **_request_data
            )
        elif method == 'post':
            response = self._rest_session.post(
                **_request_data
            )
        elif method == 'put':
            response = self._rest_session.put(
                **_request_data
            )
        elif method == 'patch':
            response = self._rest_session.patch(
                **_request_data
            )
        elif method == 'delete':
            response = self._rest_session.delete(
                **_request_data
            )
        else:
            raise UnsupportedMethodError(f'method {method} currently unsupported.')
        
        self._last_response = response
        
        if success_codes is not None and response.status_code not in success_codes:
            raise error_exc(
                f'API Error. Status code: {response.status_code}. Returned data: {response.text}'
            )
        
        if self._debug:
            app_logger.debug(
                f'''
                    -- Response --
                    Status code: {response.status_code}
                    Data: {response.content}
                '''
            )
        
        if response.text == '':
            return None

        result = BaseSDK.response_validate_json(response)

        if status_code_key is not None:
            result[status_code_key] = response.status_code
        
        return result
    
    def get_last_response(self) -> requests.Response:
        """
            Returns the last response object when calling json_endpoint.
            Useful for more details when an exception occurs.
        """
        return self._last_response

    def in_sandbox_mode(self):
        '''
            Returns True if sandbox mode is enabled
        '''
        return self._base_url == self.SANDBOX_BASE_URL

    def process_request_args(self, args: dict) -> dict:
        '''
            Adds the base url to the request url and encodes the data parameter 
            from native python dict to a string. Unpack the result of this method
            and pass it as the argument of a http request. 
            Useful for reducing boilerplate code.

            Example usage:

            ```
            requests.post(
                **process_request_args({
                    'url': 'v1/create',
                    'data' {
                        'key1': 'value1',
                        'key2': 'value2',
                    }
                })
            )
            ```
        '''
        
        args['url'] = self._base_url + args['url']
        if 'data' in args: args['data'] = json.dumps(args['data'])
        return args
    