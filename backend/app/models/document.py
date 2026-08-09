import enum
import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.user import User


class DocumentStatus(str, enum.Enum):

    UPLOADED = "uploaded"
    PROCESSING = "processing"
    PROCESSED = "processed"
    FAILED = "failed"


class Document(Base, TimestampMixin):

    __tablename__ = "documents"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    filename: Mapped[str] = mapped_column(String(255), nullable=False)

    content_type: Mapped[str] = mapped_column(String(100), nullable=False)

    size: Mapped[int] = mapped_column(Integer, nullable=False)

    storage_path: Mapped[str] = mapped_column(String(500), nullable=False, unique=True)

    status: Mapped[DocumentStatus] = mapped_column(
        default=DocumentStatus.UPLOADED,
        nullable=False,
        index=True,
    )

    # Many documents belong to one user.
    user: Mapped["User"] = relationship(back_populates="documents")

    def __repr__(self) -> str:
        return (
            f"Document(id={self.id!r}, filename={self.filename!r}, "
            f"status={self.status!r})"
        )