import dataclasses
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Cash:
    amount: int
    currency: str
    formatted_amount: str

    @classmethod
    def from_json(cls, json: dict):
        """Convert from JSON dictionary to :class:`Cash` object"""

        return cls(
            amount=json.get('amount'),
            currency=json.get('currency'),
            formatted_amount=json.get('formatted_amount')
        )


@dataclass
class Balance:
    cash: Cash
    locked_cash: Cash

    @classmethod
    def from_json(cls, json: dict):
        """Convert from JSON dictionary to :class:`Balance` object"""

        return cls(
            cash=Cash.from_json(json.get('cash')),
            locked_cash=Cash.from_json(json.get('locked_cash'))
        )


@dataclass
class _BaseRequest:
    receiver_user_id: int
    amount: int
    reference_id: str


@dataclass
class _DefaultRequest:
    sender_user_id: int = None
    note: str = None


@dataclass
class Request(_DefaultRequest, _BaseRequest):

    def to_dict(self):
        """Convert :class:`Request` object to dictionary data type"""

        return dataclasses.asdict(self)


@dataclass
class Channel:
    fee: int
    channel_id: int
    pay_code: str
    amount: int
    total: int

    @classmethod
    def from_json(cls, json: dict):
        """Convert from JSON dictionary to :class:`Channel`"""

        return cls(
            fee=int(json.get('fee')),
            channel_id=json.get('channel_id'),
            pay_code=json.get('pay_code'),
            amount=json.get('amount'),
            total=json.get('total')
        )


@dataclass
class Topup:
    channels: list[Channel]
    topup_id: str
    expires_at: datetime

    @classmethod
    def from_json(cls, json: dict):
        """Convert from JSON dictionary to :class:`Topup`"""

        expires_at = json.get('expires_at')
        if expires_at is not None:
            expires_at = datetime.utcfromtimestamp(float(expires_at))

        return cls(
            channels=list(map(lambda c: Channel.from_json(c), json.get('channels'))),
            topup_id=json.get('topup_id'),
            expires_at=expires_at
        )


@dataclass
class CashTransaction:
    cash_transaction_id: str
    user_id: str
    amount: int
    balance_before: int
    balance_after: int
    transaction_type: str
    created_at: datetime

    @classmethod
    def from_json(cls, json: dict):
        """Convert from JSON dictionary to :class:`CashTransaction`"""

        created_at = json.get('created_at')
        if created_at is not None:
            created_at = datetime.utcfromtimestamp(float(created_at))

        return cls(
            cash_transaction_id=json.get('cash_transaction_id'),
            user_id=json.get('user_id'),
            amount=json.get('amount'),
            balance_before=json.get('balance_before'),
            balance_after=json.get('balance_after'),
            transaction_type=json.get('transaction_type'),
            created_at=created_at
        )


@dataclass
class TransactionsHistory:
    cash_transactions: list[CashTransaction]
    next_page_token: str = None

    @classmethod
    def from_json(cls, json: dict):
        """Convert from JSON dictionary to :class:`TransactionHistory`"""

        if 'cash_transactions' in json:
            cash_transactions = list(
                map(lambda c: CashTransaction.from_json(c), json.get('cash_transactions'))
            )

            return cls(
                cash_transactions=cash_transactions,
                next_page_token=json.get('next_page_token') if 'next_page_token' in json else None)


@dataclass
class _BaseTransfer:
    transfer_id: str
    created_at: datetime


@dataclass
class Transfer(_DefaultRequest, _BaseRequest, _BaseTransfer):

    @classmethod
    def from_json(cls, json: dict):
        """Convert from JSON dictionary to :class:`Transfer`"""

        created_at = json.get('created_at')
        if created_at is not None:
            created_at = datetime.utcfromtimestamp(float(created_at))

        return cls(
            transfer_id=json.get('transfer_id'),
            sender_user_id=int(json.get('sender_user_id')),
            receiver_user_id=int(json.get('receiver_user_id')),
            amount=json.get('amount'),
            reference_id=json.get('reference_id'),
            note=json.get('note'),
            created_at=created_at
        )


@dataclass
class TransfersList:
    transfers: list[Transfer]
    next_page_token: str = None

    @classmethod
    def from_json(cls, json: dict):
        """Convert from JSON dictionary to :class:`TransfersList`"""

        if 'transfers' in json:
            transfers = list(map(lambda t: Transfer.from_json(t), json.get('transfers')))

            return cls(
                transfers=transfers,
                next_page_token=json.get('next_page_token') if 'next_page_token' in json else None
            )
