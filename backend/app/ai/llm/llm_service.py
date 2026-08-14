from abc import ABC, abstractmethod


class LLMService(ABC):
    """Abstract interface for Large Language Model providers."""

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """Generate a response from the provided prompt."""
        raise NotImplementedError