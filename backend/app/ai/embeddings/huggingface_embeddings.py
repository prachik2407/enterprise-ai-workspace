from langchain_huggingface import HuggingFaceEmbeddings

from app.ai.embeddings.base import BaseEmbeddingService


class HuggingFaceEmbeddingService(BaseEmbeddingService):
    """Generate embeddings using LangChain Hugging Face embeddings."""

    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2",
    ) -> None:
        self.embeddings = HuggingFaceEmbeddings(
            model_name=model_name,
        )

    def embed_text(self, text: str) -> list[float]:
        """Generate an embedding vector for a single text."""
        return self.embeddings.embed_query(text)

    def embed_texts(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        """Generate embedding vectors for multiple texts."""
        return self.embeddings.embed_documents(texts)