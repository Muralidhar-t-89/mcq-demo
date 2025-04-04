import json
import dataclasses
from datetime import datetime
from typing import Optional


@dataclasses.dataclass
class Category:
    name: str
    created_by: int
    created_date: datetime
    updated_by: Optional[int] = None
    updated_date: Optional[datetime] = None
    id: int = None

    def to_dict(self):
        dict_form = {
            "id": self.id,
            "name": self.name,
            "created_by": self.created_by,
            "created_date": self.created_date,
            "updated_by": self.updated_by,
            "updated_date": self.updated_date
        }
        return dict_form

    def to_json(self):
        dict_form = self.to_dict()
        return json.dumps(dict_form)


def build_category_from_object(series: dict) -> Category:
    """
    Converts the series representation of a category from the database into the Category entity class.

    Parameters
    ----------
    series: dict

    Returns
    -------
    Category
    """
    return Category(
        id=series["id"],
        name=series["name"],
        created_by=series["created_by"],
        created_date=series["created_date"],
        updated_by=series["updated_by"],
        updated_date=series["updated_date"]
    )
