import json
import dataclasses
from datetime import datetime


@dataclasses.dataclass
class Role:
    role_name: str
    created_date: datetime
    id: int = None

    def to_dict(self):
        dict_form = {
            "id": self.id,
            "role_name": self.role_name,
            "created_date": self.created_date
        }
        return dict_form

    def to_json(self):
        dict_form = self.to_dict()
        return json.dumps(dict_form)


def build_role_from_object(series: dict) -> Role:
    """
    Converts the series representation of a role from the database into the Role entity class.

    Parameters
    ----------
    series: dict

    Returns
    -------
    Role
    """
    return Role(
        id=series["id"],
        role_name=series["role_name"],
        created_date=series["created_date"]
    )
