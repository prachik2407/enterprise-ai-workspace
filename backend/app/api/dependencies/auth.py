import uuid

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.database.session import get_db
from app.models.user import User
from app.repositories import user_repository
from app.schemas.auth import TokenPayload
from app.utils.security import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login"
)


def _unauthorized() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


def _decode_token(token: str) -> TokenPayload:
    try:
        return decode_access_token(
            token=token,
            secret_key=settings.SECRET_KEY,
            algorithm=settings.ALGORITHM,
        )
    except (JWTError, ValidationError):
        raise _unauthorized()


def _extract_user_id(payload: TokenPayload) -> uuid.UUID:
    if payload.sub is None:
        raise _unauthorized()

    try:
        return uuid.UUID(payload.sub)
    except (ValueError, TypeError):
        raise _unauthorized()


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:

    payload = _decode_token(token)

    user_id = _extract_user_id(payload)

    user = await user_repository.get_user_by_id(
        db=db,
        user_id=user_id,
    )

    if user is None:
        raise _unauthorized()

    return user