from fastapi import APIRouter, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.schemas.auth import Token, UserCreate,UserLogin, UserResponse
from app.services import auth_service
from app.api.dependencies.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post(
        "/register",
        response_model=UserResponse,
        status_code=status.HTTP_201_CREATED,
)
async def register_user(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_db),
)-> UserResponse:
    return await auth_service.register_user(
        db=db, 
        user_in=user_in,
)

@router.post(
    "/login",
    response_model=Token,
    status_code=status.HTTP_200_OK,
)
async def login(
    user_in: UserLogin,
    db: AsyncSession = Depends(get_db),
) -> Token:
    return await auth_service.login_user(
        db=db,
        user_in=user_in,
    )

@router.post(
    "/token",
    response_model=Token,
    status_code=status.HTTP_200_OK,
)
async def token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
) -> Token:
    user_in = UserLogin(
        email=form_data.username,
        password=form_data.password,
    )

    return await auth_service.login_user(
        db=db,
        user_in=user_in,
    )

@router.get(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
async def get_me(
    current_user: User = Depends(get_current_user),
) -> UserResponse:
    return UserResponse.model_validate(current_user)