from pathlib import Path
from typing import Any
from uuid import UUID

from app.ai.chunking.text_chunker import TextChunker
from app.ai.embeddings.embedding_service import EmbeddingService
from app.ai.parsers.base import BaseParser
from app.ai.vectorstores.chroma_store import ChromaVectorStore


class DocumentIndexer:
    """Indexes parsed documents into the vector store."""

    def __init__(
        self,
        parser: BaseParser,
        chunker: TextChunker,
        embedding_service: EmbeddingService,
        vector_store: ChromaVectorStore,
    ) -> None:
        self.parser = parser
        self.chunker = chunker
        self.embedding_service = embedding_service
        self.vector_store = vector_store

    def index_document(
    self,
    file_path: Path,
    document_id: UUID | str,
    user_id: UUID | str,
    filename: str | None = None,
    ) -> int:
        """
        Parse, chunk, embed and store a document.

        Returns:
            Number of chunks indexed.
        """

        # 1. Extract text from the document
        text = self.parser.parse(file_path)

        if not text.strip():
            return 0

        # 2. Split extracted text into chunks
        chunks = self.chunker.split_text(text)

        if not chunks:
            return 0

        # 3. Extract chunk text
        chunk_texts = [
            chunk.text
            for chunk in chunks
            if chunk.text.strip()
        ]

        if not chunk_texts:
            return 0

        # 4. Generate embeddings for all chunks
        embeddings = self.embedding_service.embed_texts(
            chunk_texts
        )

        document_id_str = str(document_id)
        user_id_str = str(user_id)

        # 5. Prepare metadata and unique IDs
        metadatas: list[dict[str, Any]] = []
        ids: list[str] = []

        for index, _chunk in enumerate(chunk_texts):
            metadatas.append(
                {
                    "document_id": document_id_str,
                    "user_id": user_id_str,
                    "chunk_index": index,
                    "filename": filename or file_path.name,
                }
            )

            ids.append(
                f"{document_id_str}_{index}"
            )

        # 6. Store chunks + embeddings + metadata in Chroma
        self.vector_store.add_documents(
            texts=chunk_texts,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids,
        )

        return len(chunk_texts)