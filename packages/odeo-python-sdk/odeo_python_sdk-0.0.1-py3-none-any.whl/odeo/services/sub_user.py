from odeo.models.sub_user import *
from odeo.services.base import *


class SubUserService(BaseService):

    @authenticated
    def list_sub_users(self, page_token: str = None):
        """Retrieve paginated list of the sub users of the main account user

        :param page_token: Pagination token for next or previous sub users
        :rtype: SubUsersList
        """

        params = {'page_token': page_token} if page_token is not None else {}
        response = self.request('GET', '/sub-users', params)

        return SubUsersList.from_json(response.json())

    @authenticated
    def create_sub_user(self, email: str, name: str, phone_number: str):
        """Create a new user as the sub user of the main account user

        :param email: The sub user email address for registration
        :param name: The sub user full name
        :param phone_number: The sub user phone number where the OTP SMS will be sent to
        :return: Successfully created sub user detail
        :rtype: SubUser
        :except InputValidationError: Email address provided is invalid
        :except GeneralError: Phone number provided is already registered
        """

        response = self.request(
            'POST', '/sub-users', {'email': email, 'name': name, 'phone_number': phone_number}
        )

        return self._raise_exception_on_error(response, lambda c: SubUser.from_json(c))

    @authenticated
    def update_sub_user(self, user_id: int, email: str, name: str, phone_number: str):
        """Update specific sub user account detail

        :param user_id: The user ID of the sub user that need to be updated
        :param email: The new email address
        :param name: The new full name
        :param phone_number: The new phone number
        :rtype: SubUser
        :except InputValidationError: Email address provided is invalid
        :except GeneralError: Phone number provided is already registered
        """

        response = self.request(
            'PUT',
            f'/sub-users/{user_id}',
            {'email': email, 'name': name, 'phone_number': phone_number}
        )

        return self._raise_exception_on_error(response, lambda c: SubUser.from_json(c))
