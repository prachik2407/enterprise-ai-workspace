from abc import ABC, abstractmethod
from typing import Any


class VectorStore(ABC):
    """Abstract interface for vector store implementations."""

    @abstractmethod
    def add_documents(
        self,
        texts: list[str],
        embeddings: list[list[float]],
        metadatas: list[dict[str, Any]],
        ids: list[str],
    ) -> None:
        """Add document chunks, embeddings, metadata and IDs to the vector store."""
        raise NotImplementedError

    @abstractmethod
    def search(
    self,
    query_embedding: list[float],
    top_k: int = 5,
    user_id: str | None = None,
    ) -> list[dict[str, Any]]:
        """Search for the most similar chunks."""
        raise NotImplementedError

    @abstractmethod
    def delete_document(
        self,
        document_id: str,
    ) -> None:
        """Delete all chunks belonging to a document."""
        raise NotImplementedError