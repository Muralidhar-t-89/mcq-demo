from sqlalchemy.exc import SQLAlchemyError

from src.app.repositories.base_repository import BaseRepository
from src.app.entities.mcq import MCQ



class MCQRepository(BaseRepository):
    def __init__(self, session):
        super().__init__()
        self.session = session

    def get_one(self, item_id: int) -> MCQ:
        try:
            mcq = self.session.query(MCQ).filter(MCQ.id == item_id).first()
            return mcq
        except SQLAlchemyError as e:
            print(f"Error getting MCQ by id {item_id}: {e}")
            return None

    def get_all(self) -> list[MCQ]:
        try:
            mcqs = self.session.query(MCQ).all()
            return mcqs
        except SQLAlchemyError as e:
            print(f"Error retrieving all MCQs: {e}")
            return []

    def add(self, item: MCQ) -> bool:
        try:
            self.session.add(item)
            self.session.commit()
            return True
        except SQLAlchemyError as e:
            print(f"Error adding MCQ: {e}")
            self.session.rollback()
            return False

    def update(self, item: MCQ) -> bool:
        try:
            existing_mcq = self.get_one(item.id)
            if existing_mcq:
                existing_mcq.question = item.question
                existing_mcq.options = item.options
                existing_mcq.correct_option = item.correct_option
                existing_mcq.category = item.category
                existing_mcq.created_by = item.created_by
                existing_mcq.created_date = item.created_date
                self.session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            print(f"Error updating MCQ: {e}")
            self.session.rollback()
            return False

    def delete(self, item_id: int) -> bool:
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
