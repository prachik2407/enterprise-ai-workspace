import uuid

from app.models.user import User


def create_user(user: User) -> User:
    pass


def get_user_by_id(user_id: uuid.UUID) -> User | None:
    pass


def get_user_by_email(email: str) -> User | None:
    pass