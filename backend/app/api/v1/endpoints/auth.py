from fastapi import APIRouter, status

from app.schemas.auth import UserCreate, UserResponse

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post(
        "/register",
        response_model=UserResponse,
        status_code=status.HTTP_201_CREATED,
)
def register_user(user_in: UserCreate) -> UserResponse:
    pass