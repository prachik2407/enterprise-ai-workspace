class ContextBuilder:
    def build(self, results: list[dict]) -> str:
        """
        Combine retrieved document chunks into a single context string
        while preserving source metadata.
        """

        if not results:
            return ""

        context_parts = []

        for index, result in enumerate(results, start=1):
            text = result.get("text", "").strip()

            if not text:
                continue

            metadata = result.get("metadata", {})

            filename = metadata.get("filename", "Unknown document")
            chunk_index = metadata.get("chunk_index", "Unknown")
            document_id = metadata.get("document_id", "Unknown")

            context_parts.append(
                f"[Source {index}]\n"
                f"Document: {filename}\n"
                f"Document ID: {document_id}\n"
                f"Chunk: {chunk_index}\n"
                f"Content: {text}"
            )

        return "\n\n".join(context_parts)