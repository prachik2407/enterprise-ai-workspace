from app.ai.embeddings.base import BaseEmbeddingService
from app.ai.embeddings.huggingface_embeddings import HuggingFaceEmbeddingService
from app.ai.vectorstores.chroma_store import ChromaVectorStore


class DocumentRetriever:
    def __init__(self, top_k: int = 5, embedding_service: BaseEmbeddingService | None = None):
        self.embedding_service = embedding_service or HuggingFaceEmbeddingService()
        self.vector_store = ChromaVectorStore()
        self.top_k = top_k

    def retrieve(
    self,
    query: str,
    user_id: str | None = None,
    ) -> list[dict]:
        """
        Convert the user query into an embedding
        and retrieve the most relevant document chunks.
        """

        query_embedding = self.embedding_service.embed_text(query)

        results = self.vector_store.search(
            query_embedding,
            top_k=self.top_k,
            user_id=user_id
        )

        return results