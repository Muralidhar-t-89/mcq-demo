from sqlalchemy.orm import Session
from src.app.entities.quiz_attempt import QuizAttempt

from src.app.repositories.base_repository import BaseRepository


class QuizAttemptRepository(BaseRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_one(self, item_id: int) -> QuizAttempt:
        """
        Retrieve a single quiz attempt by its ID
        """
        return self.session.query(QuizAttempt).filter_by(id=item_id).first()

    def get_all(self) -> list[QuizAttempt]:
        """
        Retrieve all quiz attempts
        """
        return self.session.query(QuizAttempt).all()

    def add(self, quiz_attempt: QuizAttempt) -> QuizAttempt:
        """
        Add a new quiz attempt
        """
        self.session.add(quiz_attempt)
        self.session.commit()
        return quiz_attempt

    def update(self, quiz_attempt: QuizAttempt) -> QuizAttempt:
        """
        Update an existing quiz attempt
        """
        existing_attempt = self.session.query(QuizAttempt).filter_by(id=quiz_attempt.id).first()
        if existing_attempt:
            existing_attempt.score = quiz_attempt.score
            existing_attempt.questions_attempted = quiz_attempt.questions_attempted
            existing_attempt.questions_unattempted = quiz_attempt.questions_unattempted
            self.session.commit()
        return existing_attempt

    def delete(self, attempt_id: int) -> bool:
        """
        Delete a quiz attempt
        """
        quiz_attempt = self.session.query(QuizAttempt).filter_by(id=attempt_id).first()
        if quiz_attempt:
            self.session.delete(quiz_attempt)
            self.session.commit()
            return True
        return False
