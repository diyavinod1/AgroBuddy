from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class FarmerUser:
    id: str | None
    telegram_user_id: int
    name: str | None
    username: str | None
    language: str
    created_at: datetime | None = None


@dataclass(slots=True)
class PredictionResult:
    crop_name: str
    disease_name: str
    confidence: float
    symptoms: list[str]
    remedies: list[str]
    fertilizer: list[str]
    prevention: list[str]
    explanation_path: str | None = None
