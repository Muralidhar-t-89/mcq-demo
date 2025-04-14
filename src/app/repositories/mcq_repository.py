from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError

from src.app.repositories.base_repository import BaseRepository
from src.app.entities.mcq import MCQ


class MCQRepository(BaseRepository):
    def __init__(self, session):
        super().__init__()
        self.session = session

    def get_one(self, item_id: int) -> MCQ | None:
        """
        Retrieve a single MCQ by its ID
        """
        try:
            mcq = self.session.query(MCQ).filter(MCQ.id == item_id).first()
            return mcq
        except SQLAlchemyError as e:
            print(f"Error getting MCQ by id {item_id}: {e}")
            return None

    def get_all(self) -> list[MCQ]:
        """
        Retrieve all MCQs
        """
        try:
            mcqs = self.session.query(MCQ).all()
            return mcqs
        except SQLAlchemyError as e:
            print(f"Error retrieving all MCQs: {e}")
            return []

    def get_by_category(self, category_id: int) -> list[MCQ]:
        """
        Retrieve all MCQs by category ID
        """
        mcq_by_category = self.session.query(MCQ).filter(MCQ.category == category_id).all()
        return mcq_by_category

    def add(self, item: MCQ) -> bool:
        """
        Add a new MCQ to the database
        """
        try:
            self.session.add(item)
            return True
        except SQLAlchemyError as e:
            print(f"Error adding MCQ: {e}")
            self.session.rollback()
            return False

    def update(self, item: MCQ) -> bool:
        """
        Update an existing MCQ
        """
        try:
            self.session.commit()
            self.session.refresh(item)
            return True
        except SQLAlchemyError as e:
            print(f"Error adding MCQ: {e}")
            self.session.rollback()
            return False

    def delete(self, item_id: int) -> bool:
        """
        Delete an MCQ from the database
        """
        try:
            mcq = self.get_one(item_id)
            if mcq:
                self.session.delete(mcq)
                self.session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            print(f"Error deleting MCQ with id {item_id}: {e}")
            self.session.rollback()
            return False

    def get_by_question_and_options(self, question: str, options: list[str]) -> MCQ | None:
        """
        Retrieves a MCQ from the database that matches both the question text and the provided options.
        """
        mcqs = self.session.query(MCQ).filter(func.lower(func.trim(MCQ.question)) == question).all()
        print("mcqs check:", mcqs)

        for mcq in mcqs:
            stored_options = sorted(opt.strip().lower() for opt in mcq.options)
            print("stored_options check:", stored_options)
            if stored_options == options:
                return mcq
        return None