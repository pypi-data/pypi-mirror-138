from odeo.models.disbursement import Bank, BankAccount, Disbursement
from odeo.services.base import *


class DisbursementService(BaseService):

    @authenticated
    def get_banks(self):
        """Get supported by Odeo For Business API banks list

        :return: Banks list with details like bank code, swift code, etc.
        :rtype: list[Bank]
        """

        response = self.request('GET', '/dg/v1/banks')
        content = response.json()

        if response.status_code == 200 and 'banks' in content:
            return list(map(lambda bank: Bank.from_json(bank), content['banks']))

    @authenticated
    def bank_account_inquiry(
            self,
            account_number: str,
            bank_id: int,
            customer_name: str,
            with_validation: bool = False
    ):
        """Inquire bank account detail info

        :param account_number: Bank account number to inquire the info for
        :param bank_id: Supported bank ID retrieved from :func:`DisbursementService.get_banks`
        :param customer_name: Customer name that will be matched against the acquired bank info
        :param with_validation: Whether to calculate customer name matching rate
        :return: Bank account data model if inquiry is successful
        :rtype: BankAccount
        :except InputValidationError: The account number contains non-numeric characters
        :except InvalidBankError: The bank ID is not supported or invalid
        :except InsufficientBalanceError: Insufficient balance to cover inquiry fee
        """

        response = self.request('POST', '/dg/v1/bank-account-inquiry', {
            'account_number': account_number,
            'bank_id': bank_id,
            'customer_name': customer_name,
            'with_validation': with_validation
        })

        return self._raise_exception_on_error(response, lambda c: BankAccount.from_json(c))

    @authenticated
    def create_disbursement(
            self,
            account_number: str,
            amount: int,
            bank_id: int,
            customer_name: str,
            reference_id: str,
            description: str = None
    ):
        """Create disbursement order

        :param account_number: Destination account number
        :param amount: The amount that will be disbursed
        :param bank_id: Destination supported bank ID retrieved from :func:`DisbursementService.get_banks`
        :param customer_name: Receiver customer name
        :param reference_id: Unique reference ID to be associated with the created disbursement order
        :param description: Optional description to specify additional info attached to the disbursement
        :return: Disbursement data model if order successfully created
        :rtype: Disbursement
        """

        params = {
            'account_number': account_number,
            'amount': amount,
            'bank_id': bank_id,
            'customer_name': customer_name,
            'reference_id': reference_id
        }
        if description is not None:
            params['description'] = description

        response = self.request('POST', '/dg/v1/disbursements', params)

        return self._raise_exception_on_error(response, lambda c: Disbursement.from_json(c))

    @authenticated
    def get_disbursement(
            self, by_disbursement_id: int = None, by_reference_id: str = None
    ):
        """Get specific disbursement detail by its ID or reference ID

        :param by_disbursement_id: The ID of the disbursement detail retrieved
        :param by_reference_id: The reference ID of the disbursement detail retrieved
        :return: Disbursement data model if exists
        :rtype: Disbursement
        :raise ResourceNotFoundError: The disbursement with the specified ID or reference ID does not exist
        """

        assert (by_disbursement_id is not None) ^ (by_reference_id is not None), \
            'by_disbursement_id and by_reference_id parameters are mutually exclusive'

        path = f"/dg/v1/disbursements/{by_disbursement_id}" if by_disbursement_id is not None else ''
        path = f"/dg/v1/disbursements/reference-id/{by_reference_id}" if by_reference_id is not None else path
        response = self.request('GET', path)

        return self._raise_exception_on_error(response, lambda c: Disbursement.from_json(c))
