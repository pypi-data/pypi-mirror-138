from dataclasses import dataclass


@dataclass
class SubUser:
    user_id: int
    name: str
    phone_number: str
    email: str

    @classmethod
    def from_json(cls, json: dict):
        """Convert from JSON dictionary to :class:`SubUser` object"""

        return cls(
            user_id=int(json.get('user_id')),
            name=json.get('name'),
            phone_number=json.get('phone_number'),
            email=json.get('email')
        )


@dataclass
class SubUsersList:
    sub_users: list[SubUser]
    next_page_token: str = None

    @classmethod
    def from_json(cls, json: dict):
        """Convert from JSON dictionary to :class:`SubUsersList` object"""

        if 'sub_users' in json:
            sub_users = list(map(lambda s: SubUser.from_json(s), json.get('sub_users')))

            return cls(
                sub_users=sub_users,
                next_page_token=json.get('next_page_token') if 'next_page_token' in json else None
            )
