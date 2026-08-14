class PromptBuilder:
    def build(self, question: str, context: str) -> str:
        """
        Build a prompt using the user's question
        and the retrieved document context.
        """

        return f"""
You are an AI assistant that answers questions using the provided document context.

Use only the information available in the context to answer the question.

If the answer cannot be found in the context, say:
"I could not find the answer in the provided documents."

Do not make up information.

Context:
{context}

Question:
{question}

Answer:
""".strip()