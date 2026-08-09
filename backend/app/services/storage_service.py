"""
Local filesystem storage service.

Responsible for persisting uploaded files to disk under a local
storage/uploads/ directory.

This module is intentionally isolated from:
- SQLAlchemy
- repositories
- request/response schemas
- business logic
"""

from __future__ import annotations

import shutil
import uuid
from pathlib import Path

from fastapi import UploadFile


UPLOAD_DIR: Path = Path("storage") / "uploads"


def _ensure_upload_dir(directory: Path) -> None:
    """Create the upload directory if it does not exist."""
    directory.mkdir(parents=True, exist_ok=True)


def _generate_stored_filename(
    original_filename: str | None,
) -> str:
    """Generate a unique filename while preserving the extension."""
    suffix = Path(original_filename).suffix if original_filename else ""
    return f"{uuid.uuid4().hex}{suffix}"


def save_upload_file(
    upload_file: UploadFile,
    destination_dir: Path = UPLOAD_DIR,
) -> Path:
    """
    Save an uploaded file to local storage.

    The file is copied as a stream instead of loading the entire
    file into memory.
    """
    _ensure_upload_dir(destination_dir)

    stored_filename = _generate_stored_filename(
        upload_file.filename
    )

    destination_path = destination_dir / stored_filename

    try:
        with destination_path.open("wb") as buffer:
            shutil.copyfileobj(
                upload_file.file,
                buffer,
            )
    finally:
        upload_file.file.close()

    return destination_path

def delete_file(
    stored_path: Path,
) -> None:
    """
    Delete a stored file from local storage.

    Missing files are ignored so cleanup remains safe and idempotent.
    """
    stored_path.unlink(missing_ok=True)