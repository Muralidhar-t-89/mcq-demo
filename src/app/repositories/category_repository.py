from sqlalchemy.orm import Session

from src.app.entities.category import Category
from src.app.repositories.base_repository import BaseRepository


class CategoryRepository(BaseRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_one(self, item_id: int):
        """
        Retrieve a single category by ID
        """
        selected_category = self.session.query(Category).filter_by(id=item_id).first()
        if selected_category is not None:
            return selected_category
        else:
            return None

    def get_all(self) -> list[Category]:
        """
        Retrieve all categories
        """
        return self.session.query(Category).all()

    def add(self, category: Category) -> Category:
        """
        Add a new category to the database
        """
        self.session.add(category)
        self.session.commit()
        return category

    def update(self, category: Category):
        """
        Update an existing category
        """
        existing_category = self.session.query(Category).filter_by(id=category.id).first()
        if existing_category:
            existing_category.name = category.name
            existing_category.created_by = category.created_by
            self.session.commit()
        return existing_category

    def delete(self, category_id: int) -> bool:
        """
        Delete a category from the database
        """
        category = self.session.query(Category).filter_by(id=category_id).first()
        if category:
            self.session.delete(category)
            self.session.commit()
            return True
        return False
