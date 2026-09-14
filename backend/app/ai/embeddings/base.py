from abc import ABC, abstractmethod


class BaseEmbeddingService(ABC):
    """Application-level interface for text embedding services."""

    @abstractmethod
    def embed_text(self, text: str) -> list[float]:
        """Generate an embedding vector for a single text."""
        raise NotImplementedError

    @abstractmethod
    def embed_texts(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        """Generate embedding vectors for multiple texts."""
        raise NotImplementedError