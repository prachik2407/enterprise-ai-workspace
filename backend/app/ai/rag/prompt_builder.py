from app.ai.prompts.rag_prompt import RAGPrompt


class PromptBuilder:
    """Application-level wrapper for the RAG prompt."""

    def __init__(self) -> None:
        self.rag_prompt = RAGPrompt()

    def build(
        self,
        question: str,
        context: str,
    ) -> str:
        """Build an LLM-ready RAG prompt."""

        return self.rag_prompt.build(
            question=question,
            context=context,
        )