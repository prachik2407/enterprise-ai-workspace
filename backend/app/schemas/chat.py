from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    question: str = Field(min_length=2, max_length=2000, strip_whitespace=True)


class ChatSource(BaseModel):
    document: str
    document_id: str
    chunk: str


class ChatResponse(BaseModel):
    answer: str
    sources: list[ChatSource]
