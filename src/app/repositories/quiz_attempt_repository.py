from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from src.app.entities.quiz_attempt import QuizAttempt
from src.app.repositories.base_repository import BaseRepository


class QuizAttemptRepository(BaseRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_one(self, item_id: int) -> QuizAttempt | None:
        """
        Retrieve a single quiz attempt by its ID
        """
        return self.session.query(QuizAttempt).filter_by(id=item_id).first()

    def get_all(self) -> list[QuizAttempt]:
        """
        Retrieve all quiz attempts
        """
        return self.session.query(QuizAttempt).all()

    def get_by_user(self, user_id: int) -> list[QuizAttempt]:
        """
        Retrieve all quiz attempts for a specific user
        """
        return self.session.query(QuizAttempt).filter(QuizAttempt.user_id == user_id).all()

    def get_by_attempt_id(self, attempt_id: int) -> QuizAttempt | None:
        """
        Retrieve a quiz attempt by its attempt ID
        """
        return self.session.query(QuizAttempt).filter_by(attempt_id=attempt_id).first()

    def add(self, quiz_attempt: QuizAttempt) -> QuizAttempt:
        """
        Add a new quiz attempts to the database
        """
        self.session.add(quiz_attempt)
        self.session.commit()
        return quiz_attempt

    def update(self, quiz_attempt: QuizAttempt) -> bool:
        """
        Update an existing quiz attempt
        """
        try:
            existing_attempt = self.get_one(quiz_attempt.id)
            if existing_attempt:
                return False
            existing_attempt.score = quiz_attempt.score
            existing_attempt.questions_attempted = quiz_attempt.questions_attempted
            existing_attempt.questions_unattempted = quiz_attempt.questions_unattempted
            self.session.commit()
            return True
        except SQLAlchemyError as e:
            print(f"Error updating QuizAttempt: {e}")
            self.session.rollback()
            return False

    def delete(self, attempt_id: int) -> bool:
        """
        Delete a quiz attempt
        """
        try:
            quiz_attempt = self.get_one(attempt_id)
            if quiz_attempt:
                self.session.delete(quiz_attempt)
                self.session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            print(f"Error updating QuizAttempt: {e}")
            self.session.rollback()
            return False