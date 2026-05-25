from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str
    service: str
    environment: str


class ChatRequest(BaseModel):
    telegram_user_id: int
    message: str = Field(min_length=1)
    language: str | None = None


class ChatResponse(BaseModel):
    response: str
    language: str


class PredictionResponse(BaseModel):
    crop_name: str
    disease_name: str
    confidence: float
    symptoms: list[str]
    remedies: list[str]
    fertilizer: list[str]
    prevention: list[str]
    explanation_path: str | None = None


class HistoryItem(BaseModel):
    message: str | None = None
    response: str | None = None
    crop_name: str | None = None
    disease_name: str | None = None
    confidence: float | None = None
    timestamp: str | None = None
