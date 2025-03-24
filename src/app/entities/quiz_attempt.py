import json
import dataclasses
from datetime import datetime


@dataclasses.dataclass
class QuizAttempt:
    user_id: int
    attempt_id: int
    category_id: int
    total_questions: int
    questions_attempted: int
    questions_unattempted: int
    correct_answers: int
    score: int
    created_date: datetime
    id: int = None

    def to_dict(self):
        dict_form = {
            "id": self.id,
            "user_id": self.user_id,
            "attempt_id": self.attempt_id,
            "category_id": self.category_id,
            "total_questions": self.total_questions,
            "questions_attempted": self.questions_attempted,
            "questions_unattempted": self.questions_unattempted,
            "correct_answers": self.correct_answers,
            "score": self.score,
            "created_date": self.created_date
        }
        return dict_form

    def to_json(self):
        dict_form = self.to_dict()
        return json.dumps(dict_form)


def build_quiz_attempt_from_object(series: dict) -> QuizAttempt:
    """
    Converts the series representation of a quiz attempt from the database into the QuizAttempt entity class.

    Parameters
    ----------
    series: dict

    Returns
    -------
    QuizAttempt
    """
    return QuizAttempt(
        id=series["id"],
        user_id=series["user_id"],
        attempt_id=series["attempt_id"],
        category_id=series["category_id"],
        total_questions=series["total_questions"],
        questions_attempted=series["questions_attempted"],
        questions_unattempted=series["questions_unattempted"],
        correct_answers=series["correct_answers"],
        score=series["score"],
        created_date=series["created_date"]
    )
