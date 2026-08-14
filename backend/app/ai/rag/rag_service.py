from app.ai.rag.context_builder import ContextBuilder
from app.ai.rag.prompt_builder import PromptBuilder
from app.ai.rag.retriever import DocumentRetriever


class RAGService:
    """Orchestrates retrieval and prompt construction."""

    def __init__(
        self,
        top_k: int = 5,
    ) -> None:
        self.retriever = DocumentRetriever(top_k=top_k)
        self.context_builder = ContextBuilder()
        self.prompt_builder = PromptBuilder()

    def build_prompt(self, question: str) -> str:
        """
        Retrieve relevant chunks and build an LLM-ready prompt.
        """

        results = self.retriever.retrieve(question)

        context = self.context_builder.build(results)

        return self.prompt_builder.build(
            question=question,
            context=context,
        )