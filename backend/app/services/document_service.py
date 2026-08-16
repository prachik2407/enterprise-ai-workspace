"""
Document service.

Orchestrates the document upload workflow:
1. Validate the uploaded file.
2. Save the file using storage_service.
3. Validate the saved file size.
4. Create document metadata using document_repository.
5. Clean up the stored file if database persistence fails.
"""

from __future__ import annotations

from pathlib import Path
from uuid import UUID

from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.document import Document, DocumentStatus
from app.repositories import document_repository
from app.schemas.document import DocumentResponse, DocumentUploadResponse
from app.services import storage_service

from app.ai.chunking.text_chunker import TextChunker
from app.ai.embeddings.embedding_service import EmbeddingService
from app.ai.indexing.document_indexer import DocumentIndexer
from app.ai.parsers.docx_parser import DOCXParser
from app.ai.parsers.pdf_parser import PDFParser
from app.ai.parsers.tabular_parser import TabularParser
from app.ai.vectorstores.chroma_store import ChromaVectorStore


# Maximum allowed file size: 25 MB
MAX_FILE_SIZE_BYTES: int = 25 * 1024 * 1024


# Allowed MIME types
ALLOWED_CONTENT_TYPES: set[str] = {
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "text/csv",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
}

def _get_parser(file_path: Path):
    """Return the appropriate parser for the uploaded file."""

    suffix = file_path.suffix.lower()

    if suffix == ".pdf":
        return PDFParser()

    if suffix == ".docx":
        return DOCXParser()

    if suffix in {".csv", ".xlsx"}:
        return TabularParser()

    raise ValueError(
        f"Unsupported file extension: {suffix}"
    )

class InvalidFileTypeError(ValueError):
    """Raised when an uploaded file type is not supported."""


class FileTooLargeError(ValueError):
    """Raised when an uploaded file exceeds the maximum size."""


def _validate_content_type(upload_file: UploadFile) -> None:
    """Validate that the uploaded file has an allowed content type."""

    if upload_file.content_type not in ALLOWED_CONTENT_TYPES:
        allowed = ", ".join(sorted(ALLOWED_CONTENT_TYPES))

        raise InvalidFileTypeError(
            f"Unsupported content type '{upload_file.content_type}'. "
            f"Allowed types: {allowed}"
        )


def _validate_file_size(
    stored_path: Path,
    max_size_bytes: int,
) -> int:
    """
    Get the stored file size and validate the configured limit.
    """

    size = stored_path.stat().st_size

    if size > max_size_bytes:
        raise FileTooLargeError(
            f"File size {size} bytes exceeds the maximum "
            f"of {max_size_bytes} bytes."
        )

    return size


def _cleanup_stored_file(stored_path: Path) -> None:
    """Remove the stored file after a failed operation."""

    stored_path.unlink(missing_ok=True)


async def upload_document(
    db: AsyncSession,
    upload_file: UploadFile,
    user_id: UUID,
    max_file_size_bytes: int = MAX_FILE_SIZE_BYTES,
) -> DocumentUploadResponse:
    """
    Validate, store and persist metadata for an uploaded document.
    """

    # Keep these values before the storage service closes the file.
    filename = upload_file.filename or "unnamed_file"
    content_type = upload_file.content_type or "application/octet-stream"

    # 1. Validate content type
    _validate_content_type(upload_file)

    # 2. Save file to local storage
    stored_path = storage_service.save_upload_file(upload_file)

    try:
        # 3. Validate saved file size
        size = _validate_file_size(
            stored_path,
            max_file_size_bytes,
        )

        # 4. Create Document ORM object
        document = Document(
            user_id=user_id,
            filename=filename,
            content_type=content_type,
            size=size,
            storage_path=str(stored_path),
            status=DocumentStatus.UPLOADED,
        )

        # 5. Persist document metadata
        created_document = await document_repository.create_document(
            db=db,
            document=document,
        )

        # 6. Index the document for RAG
        parser = _get_parser(stored_path)

        indexer = DocumentIndexer(
            parser=parser,
            chunker=TextChunker(),
            embedding_service=EmbeddingService(),
            vector_store=ChromaVectorStore(),
        )

        indexer.index_document(
            file_path=stored_path,
            document_id=created_document.id,
            user_id=user_id,
            filename=filename,
        )

    except Exception:
        # If DB operation or size validation fails,
        # remove the already-saved file.
        _cleanup_stored_file(stored_path)
        raise

    return DocumentUploadResponse.model_validate(created_document)

async def list_user_documents(
    db: AsyncSession,
    user_id: UUID,
) -> list[DocumentResponse]:
    """
    Return all documents belonging to the authenticated user.
    """
    documents = await document_repository.list_documents_by_user(
        db=db,
        user_id=user_id,
    )

    return [
        DocumentResponse.model_validate(document)
        for document in documents
    ]


async def get_user_document(
    db: AsyncSession,
    document_id: UUID,
    user_id: UUID,
) -> DocumentResponse:
    """
    Return a document only if it belongs to the authenticated user.

    A missing document and a document belonging to another user are
    intentionally treated the same way to avoid leaking resource existence.
    """
    document = await document_repository.get_document_by_id(
        db=db,
        document_id=document_id,
    )

    if document is None or document.user_id != user_id:
        raise ValueError("Document not found")

    return DocumentResponse.model_validate(document)


async def delete_user_document(
    db: AsyncSession,
    document_id: UUID,
    user_id: UUID,
) -> None:
    """
    Delete a document only if it belongs to the authenticated user.

    Both the database record and the physical file are removed.
    """
    document = await document_repository.get_document_by_id(
        db=db,
        document_id=document_id,
    )

    if document is None or document.user_id != user_id:
        raise ValueError("Document not found")

    storage_path = Path(document.storage_path)

    # Delete the database record first.
    await document_repository.delete_document(
        db=db,
        document=document,
    )

    # Then delete the physical file.
    storage_service.delete_file(storage_path)