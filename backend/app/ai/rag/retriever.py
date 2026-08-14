from app.ai.embeddings.embedding_service import EmbeddingService
from app.ai.vectorstores.chroma_store import ChromaVectorStore


class DocumentRetriever:
    def __init__(self, top_k: int = 5):
        self.embedding_service = EmbeddingService()
        self.vector_store = ChromaVectorStore()
        self.top_k = top_k

    def retrieve(self, query: str) -> list[dict]:
        """
        Convert the user query into an embedding
        and retrieve the most relevant document chunks.
        """

        query_embedding = self.embedding_service.embed_text(query)

        results = self.vector_store.search(
            query_embedding,
            top_k=self.top_k,
        )

        return results