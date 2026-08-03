from fastapi import APIRouter, status, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.schemas.auth import UserCreate, UserResponse
from app.services import auth_service

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