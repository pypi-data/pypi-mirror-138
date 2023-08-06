class GeneralError(Exception):
    """General/generic error message"""

    error_code: int = 10000


class InputValidationError(Exception):
    """Request inputs validation failed"""

    error_code: int = 10001


class InsufficientBalanceError(Exception):
    """User balance is insufficient to cover any cash transactions"""

    error_code: int = 40011


class InvalidBankError(Exception):
    """Unsupported or invalid bank ID"""

    error_code: int = 40002


class ResourceNotFoundError(Exception):
    """The resource requested does not exists"""

    error_code: int = 20002
