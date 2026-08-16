from typing import Any

import chromadb

from app.ai.vectorstores.base import VectorStore


class ChromaVectorStore(VectorStore):
    """ChromaDB implementation of the vector store."""

    def __init__(
        self,
        persist_directory: str = "storage/chroma",
        collection_name: str = "documents",
    ) -> None:
        self.client = chromadb.PersistentClient(
            path=persist_directory
        )

        self.collection = self.client.get_or_create_collection(
            name=collection_name
        )

    def add_documents(
        self,
        texts: list[str],
        embeddings: list[list[float]],
        metadatas: list[dict[str, Any]],
        ids: list[str],
    ) -> None:
        """Add document chunks and their embeddings to Chroma."""

        self.collection.add(
            ids=ids,
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas,
        )

    def search(
        self,
        query_embedding: list[float],
        top_k: int = 5,
        user_id: str | None = None,
    ) -> list[dict[str, Any]]:
        """Search for the most similar document chunks."""

        where = None

        if user_id is not None:
            where = {"user_id": user_id}

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=where,
        )

        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]
        ids = results.get("ids", [[]])[0]

        return [
            {
                "id": ids[index],
                "text": documents[index],
                "metadata": metadatas[index],
                "distance": distances[index],
            }
            for index in range(len(documents))
        ]

    def delete_document(
        self,
        document_id: str,
    ) -> None:
        """Delete all chunks belonging to a document."""

        self.collection.delete(
            where={"document_id": document_id}
        )