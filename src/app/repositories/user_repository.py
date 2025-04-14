from sqlalchemy import func, literal
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from src.app.entities.user import User


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, user: User) -> bool:
        """
        Adds a new user to the database.

        Returns
        -------
        bool
            True if user added successfully, if not False.
        """
        try:
            self.session.add(user)
            self.session.commit()
            return True
        except SQLAlchemyError as e:
            print(f"Error adding user: {e}")
            self.session.rollback()
            return False

    def get_by_email(self, email: str) -> User | None:
        """
        Retrieves a user by email.

        Returns
        -------
        User
            The user if found, None if not.
        """
        try:
            # clean up the extra quotes before searching!
            search_email = email.strip().strip('\"')
            print("Email repr:", repr(search_email))

            user = self.session.query(User).filter(
                func.lower(User.email) == func.lower(literal(search_email))).first()
            print("user found or not:", user)

            return user
        except SQLAlchemyError as e:
            print(f"Error fetching user by email {email}: {e}")
            return None

    def get_by_id(self, user_id: int) -> User | None:
        """
        Retrieves a user by user_id.

        Returns
        -------
        User
            The user if found, None if not.
        """
        try:
            return self.session.query(User).filter(User.id == user_id).first()
        except SQLAlchemyError as e:
            print(f"Error fetching user by ID {user_id}: {e}")
            return None
