from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from src.app.entities.quiz_attempt_questions import AttemptQuestion
from src.app.repositories.base_repository import BaseRepository


class AttemptQuestionRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__()
        self.session = session

    def get_one(self, item_id: int) -> AttemptQuestion | None:
        """
        Retrieve a single Quiz Attempt Question by its ID.
        """
        try:
            quiz_attempt_by_id = (self.session.query(AttemptQuestion).filter_by(id=item_id).first())
            return quiz_attempt_by_id

        except SQLAlchemyError:
            self.session.rollback()
            return None

    def get_all(self) -> list[AttemptQuestion]:
        """
        Retrieve all Quiz Attempt Question records.
        """
        try:
            all_attempts = self.session.query(AttemptQuestion).all()
            return all_attempts
        except SQLAlchemyError:
            self.session.rollback()
            return []

    def add(self, item: AttemptQuestion) -> AttemptQuestion:
        """
        Add a new Quiz Attempt Question to the session.
        """
        try:
            self.session.add(item)
            self.session.flush()
            return item
        except SQLAlchemyError:
            self.session.rollback()
            raise

    def get_by_attempt(self, attempt_id: int) -> list[AttemptQuestion]:
        """
        Retrieve all Quiz Attempt Question rows for a given attempt_id.
        """
        try:
            all_attempt_rows = (
                self.session.query(AttemptQuestion)
                .filter_by(attempt_id=attempt_id)
                .all()
            )
            return all_attempt_rows
        except SQLAlchemyError:
            self.session.rollback()
            return []

    def delete_by_attempt(self, attempt_id: int) -> int:
        """
        Delete all Quiz Attempt Question rows for a given attempt_id.
        Returns the number of rows deleted.
        """
        try:
            count = (
                self.session
                    .query(AttemptQuestion)
                    .filter_by(attempt_id=attempt_id)
                    .delete(synchronize_session=False)
            )
            return count
        except SQLAlchemyError:
            self.session.rollback()
            raise
