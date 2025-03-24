import json
import dataclasses
from datetime import datetime
from typing import List


@dataclasses.dataclass
class MCQ:
    question: str
    options: List[str]
    correct_option: List[str]
    category: str
    created_by: int
    created_date: datetime
    id: int = None

    def to_dict(self):
        dict_form = {
            "id":self.id,
            "question": self.question,
            "options": self.options,
            "correct_option": self.correct_option,
            "category": self.category,
            "created_by": self.created_by,
            "created_date": self.created_date
        }

        return dict_form

    def to_json(self):
        dict_form = self.to_dict()
        return json.dumps(dict_form)

def build_mcq_from_object(series: dict) -> MCQ:
    """
    Converts the series representation of a mcq from the database into the MCQ entity class

    Parameters
    ----------
    series: dict

    Returns
    -------
    MCQ
    """
    return MCQ(
        id=series["id"],
        question=series["question"],
        options=series["options"],
        correct_option=series["correct_option"],
        category=series["category"],
        created_by=series["created_by"],
        created_date=series["created_date"]
    )