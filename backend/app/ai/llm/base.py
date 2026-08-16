from abc import ABC, abstractmethod


class LLMProvider(ABC):
    """
    Provider-independent interface for Large Language Models.

    Concrete providers such as Azure OpenAI, OpenAI, or Gemini
    should implement this interface.
    """

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """
        Generate a response from the given prompt.

        Args:
            prompt: Prompt containing instructions and context.

        Returns:
            Generated text response.
        """
        pass