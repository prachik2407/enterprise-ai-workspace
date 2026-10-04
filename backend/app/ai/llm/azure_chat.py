from app.core.config import settings

from langchain_openai import ChatOpenAI

from app.ai.llm.base import LLMProvider


class AzureChatProvider(LLMProvider):
    """LangChain chat model implementation for Microsoft Foundry."""

    def __init__(self) -> None:
        endpoint = settings.AZURE_OPENAI_ENDPOINT
        api_key = settings.AZURE_OPENAI_API_KEY
        deployment = settings.AZURE_OPENAI_CHAT_DEPLOYMENT

        if not endpoint:
            raise ValueError(
                "AZURE_OPENAI_ENDPOINT is not configured."
            )

        if not api_key:
            raise ValueError(
                "AZURE_OPENAI_API_KEY is not configured."
            )

        if not deployment:
            raise ValueError(
                "AZURE_OPENAI_CHAT_DEPLOYMENT is not configured."
            )

        self.llm = ChatOpenAI(
            base_url=endpoint,
            api_key=api_key,
            model=deployment,
            temperature=0,
        )

    def generate(self, prompt: str) -> str:
        """Generate a response using the LangChain chat model."""

        response = self.llm.invoke(prompt)

        return response.content or ""