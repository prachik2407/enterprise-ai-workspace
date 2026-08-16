from app.ai.llm.azure_openai import AzureOpenAIProvider
from app.ai.rag.context_builder import ContextBuilder
from app.ai.rag.prompt_builder import PromptBuilder
from app.ai.rag.retriever import DocumentRetriever


class RAGService:
    """Orchestrates retrieval, context construction and answer generation."""

    def __init__(
        self,
        top_k: int = 5,
    ) -> None:
        self.retriever = DocumentRetriever(top_k=top_k)
        self.context_builder = ContextBuilder()
        self.prompt_builder = PromptBuilder()
        self.llm = AzureOpenAIProvider()

    def build_prompt(
        self,
        question: str,
        user_id: str | None = None,
    ) -> str:
        """
        Retrieve relevant chunks and build an LLM-ready prompt.
        """

        results = self.retriever.retrieve(
            question,
            user_id=user_id,
        )

        context = self.context_builder.build(results)

        return self.prompt_builder.build(
            question=question,
            context=context,
        )

    def answer(
        self,
        question: str,
        user_id: str | None = None,
    ) -> dict:
        """
        Retrieve relevant context, generate a grounded answer,
        and return source metadata.
        """

        results = self.retriever.retrieve(
            question,
            user_id=user_id,
        )

        context = self.context_builder.build(results)

        prompt = self.prompt_builder.build(
            question=question,
            context=context,
        )

        answer = self.llm.generate(prompt)

        sources = []

        for result in results:
            metadata = result.get("metadata", {})

            sources.append(
                {
                    "document": metadata.get(
                        "filename",
                        "Unknown document",
                    ),
                    "document_id": metadata.get(
                        "document_id",
                        "Unknown",
                    ),
                    "chunk": metadata.get(
                        "chunk_index",
                        "Unknown",
                    ),
                }
            )

        return {
            "answer": answer,
            "sources": sources,
        }