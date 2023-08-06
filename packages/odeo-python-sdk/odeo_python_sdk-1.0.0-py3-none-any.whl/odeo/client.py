from functools import cached_property

from oauthlib.oauth2 import BackendApplicationClient
from requests.adapters import BaseAdapter
from requests_oauthlib import OAuth2Session

from odeo.services.base import BaseService
from odeo.services.cash import CashService
from odeo.services.disbursement import DisbursementService
from odeo.services.payment_gateway import PaymentGatewayService
from odeo.services.sub_user import SubUserService

PRODUCTION_BASE_URL = 'https://api.odeo.co.id'
DEVELOPMENT_BASE_URL = 'https://odeo-core-api.dev.odeo.co.id'


class Client(BaseService):
    """Odeo For Business API SDK client

    To create a new client object, you need to provide at the minimum
    the ``client_id``, ``client_secret``, and ``signing_key`` parameters

    Example::

        from odeo.client import Client

        client = Client(client_id='…', client_secret='…', signing_key='…')

    By default, the client will access the development API server, to access
    production API server set the ``base_url`` parameter to ``PRODUCTION_BASE_URL``
    constant

    Example::

        from odeo.client import Client, PRODUCTION_BASE_URL

        client = Client(
            client_id='…',
            client_secret='…',
            signing_key='…',
            base_url=PRODUCTION_BASE_URL
        )
    """

    client: BackendApplicationClient

    def __init__(
            self,
            client_id: str,
            client_secret: str,
            signing_key: str,
            base_url: str = DEVELOPMENT_BASE_URL
    ):
        self.client = BackendApplicationClient(client_id=client_id)

        super().__init__(
            OAuth2Session(client=self.client), base_url, client_secret, signing_key
        )

    @property
    def authentication(self) -> OAuth2Session:
        """OAuth 2 session object"""

        return self._oauth

    def set_transport_adapter(self, prefix: str, adapter: BaseAdapter):
        """Override network transport adapter used in the Requests calls"""

        self._oauth.mount(prefix, adapter)

    @cached_property
    def disbursement(self) -> DisbursementService:
        """Cached Disbursement service group object"""

        return DisbursementService(
            self._oauth, self._base_url, self._client_secret, self._signing_key
        )

    @cached_property
    def payment_gateway(self) -> PaymentGatewayService:
        """Cached Payment Gateway service group object"""

        return PaymentGatewayService(
            self._oauth, self._base_url, self._client_secret, self._signing_key
        )

    @cached_property
    def sub_user(self) -> SubUserService:
        """Cached Sub User service group object"""

        return SubUserService(
            self._oauth, self._base_url, self._client_secret, self._signing_key
        )

    @cached_property
    def cash(self) -> CashService:
        """Cached Cash service group object"""

        return CashService(
            self._oauth, self._base_url, self._client_secret, self._signing_key
        )
