from sentence_transformers import SentenceTransformer

from app.ai.embeddings.base import BaseEmbeddingService


class EmbeddingService(BaseEmbeddingService):
    """Generate vector embeddings for text."""

    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2",
    ) -> None:
        self.model = SentenceTransformer(model_name)

    def embed_text(self, text: str) -> list[float]:
        """Generate an embedding vector for a single text."""

        embedding = self.model.encode(
            text,
            convert_to_numpy=True,
        )

        return embedding.tolist()

    def embed_texts(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        """Generate embedding vectors for multiple texts."""

        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
        )

        return embeddings.tolist()