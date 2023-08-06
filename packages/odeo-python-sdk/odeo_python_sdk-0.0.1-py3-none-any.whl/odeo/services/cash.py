from datetime import datetime

from odeo.models.cash import Balance, Request, Topup, TransactionsHistory, Transfer, TransfersList
from odeo.services.base import *


class CashService(BaseService):

    @authenticated
    def create_bulk_transfers(self, requests: list[Request]):
        """Create bulk transfer orders to any users in the system

        :param requests: Transfer requests object list
        :return: Successfully created transfers order
        :rtype: list[Transfer]
        """

        params = {'requests': (list(map(lambda request: request.to_dict(), requests)))}
        response = self.request('POST', '/cash/bulk-transfer', params)

        return self._raise_exception_on_error(
            response,
            lambda c: list(map(lambda transfer: Transfer.from_json(transfer), c['transfers']))
        )

    @authenticated
    def list_transfers(
            self,
            reference_ids: list[str] = None,
            start_date: datetime = None,
            end_date: datetime = None,
            page_token: str = None
    ):
        """Retrieve paginated list of transfers history

        :param reference_ids: Filter transfers with specific reference ID
        :param start_date: Filter transfer creation date from specific date
        :param end_date: Filter transfer creation date until specific date
        :param page_token: Pagination token for next or previous transfers
        :rtype: TransfersList
        """

        params = {}

        if reference_ids is not None:
            for i in range(0, len(reference_ids)):
                params[f'reference_ids[{i}]'] = reference_ids[i]
        if start_date is not None:
            params['start_date'] = int(start_date.timestamp())
        if end_date is not None:
            params['end_date'] = int(end_date.timestamp())
        if page_token is not None:
            params['page_token'] = page_token

        response = self.request('GET', '/cash/transfers', params)

        return TransfersList.from_json(response.json())

    @authenticated
    def create_va_topup(self, amount: int, user_id: int = None):
        """Create top up order for Virtual Account payment channels

        :param amount: The amount that will be deposited
        :param user_id: Specific user ID where to deposit the amount, or current user if not set
        :return: Successfully created top up order
        :rtype: Topup
        :except InputValidationError: Minimum amount is 10000, maximum 1000000000000
        :except GeneralError: User with specified user ID not found, or there's pending top up order
        """

        params = {'amount': amount, 'user_id': user_id}
        response = self.request('POST', '/cash/va-topup', params)

        return self._raise_exception_on_error(response, lambda c: Topup.from_json(c))

    @authenticated
    def find_active_va_topup(self, user_id: int = None):
        """Retrieve currently active/pending Virtual Account top up order

        :param user_id: Specified the user ID of the top-up order
        :rtype: Topup
        :except GeneralError: There's no currently active/pending top up order
        """

        params = {'user_id': user_id} if user_id is not None else {}
        response = self.request('GET', '/cash/va-topup/active', params)

        return self._raise_exception_on_error(response, lambda c: Topup.from_json(c))

    @authenticated
    def cancel_va_topup(self, user_id: str = None):
        """Cancel currently active/pending Virtual Account top up order

        :param user_id: Specified the user ID of the top-up order
        :return: Empty dictionary if successful
        :except GeneralError: There's no currently active/pending top up order,
            or user with specified user ID not found,
            or you're not authorized to cancel the order,
            or the top-up order can't be canceled
        """

        params = {'user_id': user_id} if user_id is not None else None
        response = self.request('POST', '/cash/va-topup/cancel', params)

        return self._raise_exception_on_error(response, lambda c: c)

    @authenticated
    def get_balance(self, user_id: str = 'me'):
        """Retrieve the balance of current or specified user

        :param user_id: Specify the user ID
        :rtype: Balance
        :except GeneralError: The user with specified user ID not found
        """

        response = self.request('GET', f'/cash/{user_id}/balance')

        return self._raise_exception_on_error(response, lambda c: Balance.from_json(c))

    @authenticated
    def get_transactions_history(
            self,
            user_ids: list[int] = None,
            start_date: datetime = None,
            end_date: datetime = None,
            page_token: str = None
    ):
        """Retrieve the paginated list of transactions history for current or specified users

        :param user_ids: Specify the sub user ID
        :param start_date: Filter transaction creation date from specific date
        :param end_date: Filter transaction creation date until specific date
        :param page_token: Pagination token for next or previous transactions
        :rtype: TransactionsHistory
        """

        path = '/cash/transactions'
        params = {}

        if user_ids is not None:
            path = '/cash/sub-user-transactions'
            for i in range(0, len(user_ids)):
                params[f'user_ids[{i}]'] = user_ids[i]
        if start_date is not None:
            params['start_date'] = int(start_date.timestamp())
        if end_date is not None:
            params['end_date'] = int(end_date.timestamp())
        if page_token is not None:
            params['page_token'] = page_token

        response = self.request('GET', path, params)

        return TransactionsHistory.from_json(response.json())
