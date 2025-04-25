import logging
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.app.services.unit_of_work import MCQUnitOfWork
from src.app.schemas import user_schema
from src.app.services.user_services import UserService

logger = logging.getLogger(__name__)

user_blueprint = APIRouter()

@user_blueprint.post("/register", response_model=user_schema.UserResponse)
async def register_user(user_data: user_schema.UserCreate):
    """
    Endpoint to register a new user.

    Returns
    -------
    Returns a success message or an error response
    """
    try:
        # Call the service to create a new user
        response = await UserService.create_user(user_data=user_data, unit_of_work=MCQUnitOfWork())

        return response

    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}")
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logger.error(f"Unexpected Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@user_blueprint.post("/login", response_model=user_schema.UserLogin)
async def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Endpoint to log in and generate a JWT token.

    Returns
    -------
    dict
        Access Token (JWT)
    """
    email = form_data.username

    with MCQUnitOfWork() as uow:
        user_service = UserService(session=uow.session)

        # Authenticate the user by checking the email and password
        authenticated_user = await user_service.authenticate_user(
            email=email, password=form_data.password, unit_of_work=uow
        )

        if not authenticated_user:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        access_token = UserService.generate_jwt_token(authenticated_user)
        return {"access_token": access_token, "token_type": "bearer"}
