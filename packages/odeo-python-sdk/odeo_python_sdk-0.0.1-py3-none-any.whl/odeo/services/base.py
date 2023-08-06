import functools
import json
import time
from urllib.parse import unquote, urlencode, urljoin

from requests import Response
from requests_oauthlib import OAuth2Session

from odeo.api_signature import generate_signature
from odeo.exceptions import *


def authenticated(func):
    @functools.wraps(func)
    def wrapper_decorator(self: BaseService, *args, **kwargs):
        self.request_access_token()
        return func(self, *args, **kwargs)

    return wrapper_decorator


class BaseService(object):
    _oauth: OAuth2Session
    _base_url: str
    _client_secret: str
    _signing_key: str

    def __init__(
            self, oauth: OAuth2Session, base_url: str, client_secret: str, signing_key: str
    ):
        self._oauth = oauth
        self._base_url = base_url
        self._client_secret = client_secret
        self._signing_key = signing_key

    def request_access_token(self) -> str:
        if not self._oauth.authorized:
            self._oauth.fetch_token(
                self._base_url + '/oauth2/token',
                client_secret=self._client_secret,
                include_client_id=True
            )

        return self._oauth.access_token

    def request(
            self,
            method: str,
            path: str,
            params: dict = None
    ) -> Response | None:
        query_string = ''
        request_body = ''

        if params is not None:
            if method == 'GET':
                query_string = unquote(urlencode(sorted(params.items())))
            elif method in ['POST', 'PUT']:
                request_body = json.dumps(params, separators=(',', ':'))

        timestamp = int(time.time())
        signature = generate_signature(
            method,
            path,
            query_string,
            self._oauth.access_token,
            timestamp,
            request_body,
            self._signing_key
        )

        url = urljoin(self._base_url, path)
        headers = {
            'X-Odeo-Timestamp': str(timestamp),
            'X-Odeo-Signature': signature
        }

        if method == 'GET':
            headers |= {'Accept': 'application/json'}
            return self._oauth.get(url, params=params, headers=headers)
        elif method == 'POST':
            headers |= {'Content-Type': 'application/json'}
            return self._oauth.post(url, json=params, headers=headers)
        elif method == 'PUT':
            headers |= {'Content-Type': 'application/json'}
            return self._oauth.put(url, json=params, headers=headers)

        return None

    @staticmethod
    def _raise_exception_on_error(response: Response, success: callable):
        content = response.json()
        if response.status_code == 400 or 'error_code' in content:
            error_code = content['error_code']
            message = content['message']
            if error_code == 40002:
                raise InvalidBankError(message)
            elif error_code == 40011:
                raise InsufficientBalanceError(message)
            elif error_code == 20002:
                raise ResourceNotFoundError(message)
            elif error_code == 10001:
                raise InputValidationError(message)
            elif error_code == 10000:
                raise GeneralError(message)
        elif response.status_code == 200:
            return success(content)
