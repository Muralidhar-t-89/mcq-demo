import json
import dataclasses
from datetime import datetime


@dataclasses.dataclass
class User:
    first_name: str
    last_name: str
    email: str
    password: str
    role: int
    created_date: datetime
    id: int = None

    def to_dict(self) -> dict:
        dict_form = {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "password": self.password,
            "role": self.role,
            "created_date": self.created_date
        }
        return dict_form

    def to_json(self) -> str:
        dict_form = self.to_dict()
        return json.dumps(dict_form)


def build_user_from_object(series: dict) -> User:
    """
    Converts the series representation of a user from the database into the User entity class.

    Parameters
    ----------
    series: dict

    Returns
    -------
    User
    """
    return User(
        id=series["id"],
        first_name=series["first_name"],
        last_name=series["last_name"],
        email=series["email"],
        password=series["password"],
        role=series["role"],
        created_date=series["created_date"]
    )
