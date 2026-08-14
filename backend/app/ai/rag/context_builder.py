class ContextBuilder:
    def build(self, results: list[dict]) -> str:
        """
        Combine retrieved document chunks into a single context string.
        """

        if not results:
            return ""

        context_parts = []

        for result in results:
            text = result.get("text", "").strip()

            if text:
                context_parts.append(text)

        return "\n\n".join(context_parts)