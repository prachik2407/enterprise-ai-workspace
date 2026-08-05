from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.user import User
from app.repositories import user_repository
from app.schemas.auth import Token, UserCreate, UserLogin, UserResponse
from app.utils.security import create_access_token, hash_password, verify_password
from app.utils.helpers import normalize_email

async def register_user(
    db: AsyncSession,
    user_in: UserCreate,
) -> UserResponse:

    normalized_email = normalize_email(user_in.email)

    existing_user = await user_repository.get_user_by_email(
        db,
        normalized_email,
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    hashed_password = hash_password(user_in.password)

    user = User(
        full_name=user_in.full_name,
        email=normalized_email,
        hashed_password=hashed_password,
    )

    created_user = await user_repository.create_user(db, user)

    return UserResponse.model_validate(created_user)


async def login_user(
    db: AsyncSession,
    user_in: UserLogin,
) -> Token:

    normalized_email = normalize_email(user_in.email)

    user = await user_repository.get_user_by_email(
        db,
        normalized_email,
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    if not verify_password(
        user_in.password,
        user.hashed_password,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    access_token = create_access_token(
        data={
            "sub": str(user.id),
        },
        expires_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        secret_key=settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )


    return Token(
        access_token=access_token,
        token_type="bearer",
    )