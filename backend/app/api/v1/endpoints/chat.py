import logging
from functools import lru_cache

from fastapi import APIRouter, Depends, HTTPException, status
from starlette.concurrency import run_in_threadpool

from app.ai.rag.rag_service import RAGService
from app.api.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.chat import ChatRequest, ChatResponse

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/chat", tags=["chat"])


@lru_cache(maxsize=1)
def _get_rag_service() -> RAGService:
    return RAGService()


def _answer_question(question: str, user_id: str) -> dict:
    return _get_rag_service().answer(question, user_id)


@router.post("/ask", response_model=ChatResponse, status_code=status.HTTP_200_OK)
async def ask_question(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
) -> ChatResponse:
    """Answer a question using only the authenticated user's indexed documents."""
    try:
        result = await run_in_threadpool(
            _answer_question, request.question, str(current_user.id)
        )
        return ChatResponse.model_validate(result)
    except Exception as exc:
        # Keep secrets/provider details out of API responses.
        logger.exception("RAG chat request failed")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="The AI service could not answer this question. Check the server configuration and try again.",
        ) from exc
