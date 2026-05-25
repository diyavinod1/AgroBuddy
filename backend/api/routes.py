from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, File, Form, UploadFile, status
from fastapi.responses import FileResponse

from backend.core.config import get_settings
from backend.core.errors import http_error
from backend.schemas.api import ChatRequest, ChatResponse, HealthResponse, PredictionResponse
from backend.services.chat_service import ChatService
from backend.services.history_service import HistoryService
from backend.services.prediction_service import PredictionService
from backend.services.speech_service import SpeechService

router = APIRouter()


@router.get("/health", response_model=HealthResponse, tags=["system"])
async def health() -> HealthResponse:
    settings = get_settings()
    return HealthResponse(status="ok", service="AgroBuddy", environment=settings.app_env)


@router.post("/chat", response_model=ChatResponse, tags=["chat"])
async def chat(payload: ChatRequest) -> ChatResponse:
    response, language = await ChatService().reply(payload.telegram_user_id, payload.message, payload.language)
    return ChatResponse(response=response, language=language)


@router.post("/predict", response_model=PredictionResponse, tags=["vision"])
async def predict(telegram_user_id: int = Form(...), image: UploadFile = File(...)) -> PredictionResponse:
    if not image.content_type or not image.content_type.startswith("image/"):
        raise http_error("Upload a valid image file.", status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
    settings = get_settings()
    suffix = Path(image.filename or "leaf.jpg").suffix.lower() or ".jpg"
    image_path = settings.upload_dir / f"leaf_{uuid4().hex}{suffix}"
    image_path.write_bytes(await image.read())
    result = PredictionService().predict_for_user(telegram_user_id, image_path)
    return PredictionResponse(**result.__dict__)


@router.post("/speech-to-text", tags=["speech"])
async def speech_to_text(
    language: str = Form("en"),
    audio: UploadFile = File(...),
) -> dict[str, str]:
    settings = get_settings()
    suffix = Path(audio.filename or "voice.ogg").suffix.lower() or ".ogg"
    audio_path = settings.upload_dir / f"voice_{uuid4().hex}{suffix}"
    audio_path.write_bytes(await audio.read())
    transcript = await SpeechService().speech_to_text(audio_path, language)
    return {"text": transcript, "language": language}


@router.post("/text-to-speech", tags=["speech"])
async def text_to_speech(text: str = Form(...), language: str = Form("en")) -> FileResponse:
    audio_path = await SpeechService().text_to_speech(text, language)
    return FileResponse(audio_path, media_type="audio/mpeg", filename=Path(audio_path).name)


@router.get("/history/{telegram_user_id}", tags=["history"])
async def history(telegram_user_id: int, limit: int = 10) -> dict:
    return HistoryService().history(telegram_user_id, limit=limit)
