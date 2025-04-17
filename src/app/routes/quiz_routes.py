from fastapi import APIRouter, Depends
from typing import List

from src.app.common.utils import get_current_user
from src.app.schemas.quiz_schema import (
    QuizStartResponse,
    QuizSubmitRequest,
    QuizSubmitResponse,
    QuizAttemptResponse
)
from src.app.services.unit_of_work import MCQUnitOfWork
from src.app.services.quiz_services import QuizService

quiz_blueprint = APIRouter()


@quiz_blueprint.post("/quiz/start", response_model=QuizStartResponse)
def start_quiz(category_id: int, current_user=Depends(get_current_user)):
    """
    Start a new quiz attempt.

    Fetches up to 25 random MCQs for the given category and returns a unique attempt_id
    along with the selected questions. Only authenticated users may start a quiz.

    Parameters
    ----------
    category_id : int
        The ID of the category from which to draw questions.
    current_user : User
        Injected by the `get_current_user` dependency; must be logged in.

    Returns
    -------
    QuizStartResponse
        Contains the generated `attempt_id` and a list of `QuizQuestion` objects.
    """
    with MCQUnitOfWork() as uow:
        quiz_service = QuizService(session=uow.session)
        return quiz_service.start_quiz(current_user.id, category_id)


@quiz_blueprint.post("/quiz/submit", response_model=QuizSubmitResponse)
def submit_quiz(payload: QuizSubmitRequest, current_user=Depends(get_current_user)):
    """
    Submit answers for a quiz attempt and calculate the score.

    Validates the submitted answers against the correct answers stored in the database.

    Parameters
    ----------
    payload : QuizSubmitRequest
        The payload containing `attempt_id`, `category_id`, and list of answers.
    current_user : User
        Injected by the `get_current_user` dependency; must be logged in.

    Returns
    -------
    QuizSubmitResponse
        Summarizes the attempt: total questions, attempted, unattempted, correct,
        wrong, and the total score.
    """
    with MCQUnitOfWork() as uow:
        quiz_service = QuizService(session=uow.session)
        return quiz_service.submit_quiz(current_user.id, payload)


@quiz_blueprint.get("/quiz/attempts", response_model=List[QuizAttemptResponse])
def list_attempts(current_user=Depends(get_current_user)):
    """
    List all quiz attempts made by the current user.

    Parameters
    ----------
    current_user : User
        Injected by the `get_current_user` dependency; must be logged in.

    Returns
    -------
    List[QuizAttemptResponse]
        A list of all quiz attempts made by the current user.
    """
    with MCQUnitOfWork() as uow:
        quiz_service = QuizService(session=uow.session)
        return quiz_service.get_user_attempts(current_user)
