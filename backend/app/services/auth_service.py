from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories import user_repository
from app.schemas.auth import UserCreate, UserResponse
from app.utils.security import hash_password


async def register_user(
    db: AsyncSession,
    user_in: UserCreate,
) -> UserResponse:

    normalized_email = user_in.email.lower()

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
