from dataclasses import dataclass


@dataclass
class TextChunk:
    """Represents a chunk of extracted document text."""

    text: str
    chunk_index: int


class TextChunker:
    """Split extracted document text into overlapping chunks."""

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

    def split_text(self, text: str) -> list[TextChunk]:
        """Split text into overlapping chunks."""

        text = text.strip()

        if not text:
            return []

        chunks: list[TextChunk] = []

        start = 0
        chunk_index = 0
        text_length = len(text)

        while start < text_length:
            end = min(
                start + self.chunk_size,
                text_length,
            )

            chunk_text = text[start:end].strip()

            if chunk_text:
                chunks.append(
                    TextChunk(
                        text=chunk_text,
                        chunk_index=chunk_index,
                    )
                )

                chunk_index += 1

            if end >= text_length:
                break

            start = end - self.chunk_overlap

        return chunks