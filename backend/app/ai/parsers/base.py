from abc import ABC, abstractmethod
from pathlib import Path


class BaseParser(ABC):
    """Base interface for document parsers."""

    @abstractmethod
    def parse(self, file_path: Path) -> str:
        """Parse a document and return extracted text."""
        raise NotImplementedError