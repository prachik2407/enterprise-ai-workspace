import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.document import Document


async def create_document(
    db: AsyncSession,
    document: Document,
) -> Document:
    db.add(document)
    await db.commit()
    await db.refresh(document)
    return document


async def get_document_by_id(
    db: AsyncSession,
    document_id: uuid.UUID,
) -> Document | None:
    result = await db.execute(
        select(Document).where(Document.id == document_id)
    )
    return result.scalar_one_or_none()


async def list_documents_by_user(
    db: AsyncSession,
    user_id: uuid.UUID,
) -> list[Document]:
    result = await db.execute(
        select(Document)
        .where(Document.user_id == user_id)
        .order_by(Document.created_at.desc())
    )

    return list(result.scalars().all())


async def delete_document(
    db: AsyncSession,
    document: Document,
) -> None:
    await db.delete(document)
    await db.commit()