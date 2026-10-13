from app.ai.chunking.text_chunker import TextChunker
from app.ai.rag.context_builder import ContextBuilder


def test_text_chunker_returns_no_chunks_for_blank_text():
    assert TextChunker().split_text("  \n ") == []


def test_text_chunker_chunks_and_preserves_order():
    chunks = TextChunker(chunk_size=10, chunk_overlap=2).split_text("abcdefghijklmnopqrstuvwxyz")
    assert len(chunks) > 1
    assert chunks[0].text.startswith("abcdefghij")
    assert chunks[0].chunk_index == 0
    assert chunks[1].chunk_index == 1


def test_context_builder_includes_source_metadata_and_text():
    context = ContextBuilder().build([
        {
            "text": "Employees receive 18 days of annual paid leave.",
            "metadata": {"filename": "handbook.pdf", "document_id": "doc-1", "chunk_index": 2},
        }
    ])
    assert "handbook.pdf" in context
    assert "doc-1" in context
    assert "Chunk: 2" in context
    assert "18 days" in context


def test_context_builder_handles_empty_results():
    assert ContextBuilder().build([]) == ""
