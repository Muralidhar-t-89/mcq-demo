import random
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError, ExpiredSignatureError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from src.app.build_db import get_db
from src.app.repositories.user_repository import UserRepository
from src.app.config import settings
import bcrypt
if not hasattr(bcrypt, "__about__"):
    bcrypt.__about__ = {"__version__": "3.2.0"}


# Ref: https://medium.com/@kevinkoech265/jwt-authentication-in-fastapi-building-secure-apis-ce63f4164eb2

# Create a CryptContext instance for bcrypt hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt.
    """
    hashed = pwd_context.hash(password)
    return hashed


def verify_password(non_hashed_password: str, hashed_password: str) -> bool:
    """
    Verify that a plain password matches a hashed password.
    """
    print("Verifying the password against the hash..!")
    # print("non hashed pwd:", repr(non_hashed_password))
    # print("hashed_password:", repr(hashed_password))
    verified_pwd = pwd_context.verify(non_hashed_password.strip('\"'), hashed_password.strip())
    return verified_pwd


def verify_token_access(token: str, credentials_exception) -> dict:
    """
    Verifies the given JWT token and extracts user details
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

        user_id: str = payload.get("sub")
        print("verifying the token..!")
        email: str = payload.get("email")
        role: int = payload.get("role")

        if user_id is None or email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user_details = {"id": user_id, "email": email, "role": role}
        print("user_details:", user_details)
        return user_details

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired. Please log in again.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    except JWTError as e:
        print(e)
        raise credentials_exception

def get_current_user(token: str = Depends(oauth2_scheme),
                     db: Session = Depends(get_db),
                     require_admin: bool = False):
    """
    Extracts the current user from the token and verifies if they have admin access.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    # from jose import jwt
    # token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxNSIsImV4cCI6MTc0MzUxMTk5MywiZW1haWwiOiJjaGFuLmFAZ21haWwuY29tIiwicm9sZSI6Mn0.8dav5hHajXc4ABNQVmJGdCDttKJxHURUTlgzKu9qIno"
    # decoded_payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    # print("Decoded JWT payload:", decoded_payload)

    token = verify_token_access(token, credentials_exception)
    if not token:
        raise credentials_exception

    try:
        user_id = int(token.get("id"))
    except (TypeError, ValueError):
        raise credentials_exception
    user_repo = UserRepository(db)
    user = user_repo.get_by_id(user_id)
    print("user:", user)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if require_admin and user.role != 1:
        raise HTTPException(status_code=403, detail="Admin access required")

    return user

def generate_unique_attempt_id(attempt_repo):
    """
    Generate a unique 6-digit attempt ID for the user.
    """
    while True:
        attempt_id = random.randint(100000, 999999)
        existing_attempt = attempt_repo.get_by_attempt_id(attempt_id)
        if not existing_attempt:
            return attempt_id
