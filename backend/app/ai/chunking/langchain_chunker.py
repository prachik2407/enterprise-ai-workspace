from app.ai.chunking.text_chunker import TextChunk

from langchain_text_splitters import RecursiveCharacterTextSplitter


class LangChainTextChunker:
    """Split extracted document text using LangChain."""

    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ) -> None:
        if chunk_size <= 0:
            raise ValueError("chunk_size must be greater than 0")

        if chunk_overlap < 0:
            raise ValueError("chunk_overlap cannot be negative")

        if chunk_overlap >= chunk_size:
            raise ValueError(
                "chunk_overlap must be smaller than chunk_size"
            )

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

    def split_text(self, text: str) -> list[TextChunk]:
        """Split extracted document text into overlapping chunks."""

        text = text.strip()

        if not text:
            return []

        split_texts = self.splitter.split_text(text)

        return [
            TextChunk(
                text=chunk,
                chunk_index=index,
            )
            for index, chunk in enumerate(split_texts)
            if chunk.strip()
        ]