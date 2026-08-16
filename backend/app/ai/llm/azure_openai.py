import os

from openai import OpenAI

from app.ai.llm.base import LLMProvider


class AzureOpenAIProvider(LLMProvider):
    """Azure OpenAI implementation of the LLMProvider interface."""

    def __init__(self):
        endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        api_key = os.getenv("AZURE_OPENAI_API_KEY")
        deployment = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT")

        if not endpoint:
            raise ValueError("AZURE_OPENAI_ENDPOINT is not configured.")

        if not api_key:
            raise ValueError("AZURE_OPENAI_API_KEY is not configured.")

        if not deployment:
            raise ValueError(
                "AZURE_OPENAI_CHAT_DEPLOYMENT is not configured."
            )

        base_url = endpoint.rstrip("/")

        if not base_url.endswith("/openai/v1"):
            base_url = f"{base_url}/openai/v1"

        self.client = OpenAI(
            api_key=api_key,
            base_url=f"{base_url}/",
        )

        self.deployment = deployment

    def generate(self, prompt: str) -> str:
        """Generate a response using the deployed Azure OpenAI model."""

        response = self.client.chat.completions.create(
            model=self.deployment,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        return response.choices[0].message.content or ""