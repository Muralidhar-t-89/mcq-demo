import logging
from datetime import datetime, timedelta
from fastapi import HTTPException
from jose import jwt
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.app.repositories.user_repository import UserRepository
from src.app.entities.user import User
from src.app.common.utils import verify_password, hash_password
from src.app.schemas.user_schema import UserCreate, UserResponse
from src.app.config import settings

logger = logging.getLogger(__name__)

ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
ALGORITHM = settings.ALGORITHM
SECRET_KEY = settings.SECRET_KEY


class UserService:
    def __init__(self, session: Session):
        self.repository = UserRepository(session)

    @staticmethod
    async def create_user(user_data: UserCreate, unit_of_work):
        """
        Creates a new user and stores it in the database.
        """
        with unit_of_work as uow:
            # Check if user already exists
            existing_user = uow.user_repo.get_by_email(user_data.email)
            if existing_user:
                logger.error(f"User with email {user_data.email} already exists.")
                raise HTTPException(status_code=400, detail="User with this email already exists.")

            # Hash the password before saving the user
            hashed_password = hash_password(user_data.password)

            user = User(
                first_name=user_data.first_name,
                last_name=user_data.last_name,
                email=str(user_data.email),
                password=hashed_password,
                role=user_data.role,
                created_date=datetime.now(),
            )
            print("user:", user)
            try:
                uow.user_repo.add(user)
                uow.commit()
                uow.session.refresh(user)
                print(f"User {user.email} registered successfully with ID {user.id}")
                return UserResponse(message="User registered successfully!", user_id=user.id)

            except IntegrityError as e:
                uow.rollback()
                logger.error(f"Database IntegrityError: {e}")
                raise HTTPException(status_code=400, detail="User creation failed. Please try again.")

            except Exception as e:
                logger.error(f"Unexpected error during user creation: {e}")
                raise HTTPException(status_code=500, detail="Internal Server Error")


    async def authenticate_user(self, email: str, password: str, unit_of_work) -> User | None:
        """
        Authenticate a user by verifying email and password.
        """
        user = unit_of_work.user_repo.get_by_email(email)

        if user and verify_password(password, user.password):
            print("User authenticated successfully.")
            return user

        return None

    @staticmethod
    def generate_jwt_token(user: User) -> str:
        """
        Generates a JWT token for the authenticated user.
        """
        expiration = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        payload = {
            "sub": str(user.id),
            "exp": expiration,
            "email": user.email,
            "role": user.role,
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        print("Generated JWT token:", token)
        return token
