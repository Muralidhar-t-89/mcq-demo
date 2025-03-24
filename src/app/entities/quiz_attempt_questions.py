import json
import dataclasses


@dataclasses.dataclass
class AttemptQuestion:
    attempt_id: str
    question_id: int
    attempted_answer: str
    is_correct: bool
    id: int = None

    def to_dict(self):
        dict_form = {
            "id": self.id,
            "attempt_id": self.attempt_id,
            "question_id": self.question_id,
            "attempted_answer": self.attempted_answer,
            "is_correct": self.is_correct
        }
        return dict_form

    def to_json(self):
        dict_form = self.to_dict()
        return json.dumps(dict_form)


def build_attempt_question_from_object(series: dict) -> AttemptQuestion:
    """
    Converts the series representation of an attempt question from the database into the AttemptQuestion entity class.

    Parameters
    ----------
    series: dict

    Returns
    -------
    AttemptQuestion
    """
    return AttemptQuestion(
        id=series["id"],
        attempt_id=series["attempt_id"],
        question_id=series["question_id"],
        attempted_answer=series["attempted_answer"],
        is_correct=series["is_correct"]
    )
