from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    telegram_bot_token: str = Field(default="", alias="TELEGRAM_BOT_TOKEN")
    llm_api_key: str = Field(default="", alias="LLM_API_KEY")
    sarvam_api_key: str = Field(default="", alias="SARVAM_API_KEY")
    supabase_url: str = Field(default="", alias="SUPABASE_URL")
    supabase_key: str = Field(default="", alias="SUPABASE_KEY")
    jwt_secret: str = Field(default="", alias="JWT_SECRET")

    app_env: str = Field(default="development", alias="APP_ENV")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    api_host: str = Field(default="0.0.0.0", alias="API_HOST")
    api_port: int = Field(default=8000, alias="API_PORT")
    upload_dir: Path = Field(default=Path("uploads"), alias="UPLOAD_DIR")
    model_path: Path = Field(default=Path("models/plant_disease_model.keras"), alias="MODEL_PATH")
    model_labels_path: Path = Field(default=Path("models/labels.json"), alias="MODEL_LABELS_PATH")
    llm_model: str = Field(default="openai/gpt-4o-mini", alias="LLM_MODEL")
    sarvam_stt_url: str = Field(default="https://api.sarvam.ai/speech-to-text", alias="SARVAM_STT_URL")
    sarvam_tts_url: str = Field(default="https://api.sarvam.ai/text-to-speech", alias="SARVAM_TTS_URL")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @property
    def supabase_enabled(self) -> bool:
        return bool(self.supabase_url and self.supabase_key)

    @property
    def llm_enabled(self) -> bool:
        return bool(self.llm_api_key)

    @property
    def sarvam_enabled(self) -> bool:
        return bool(self.sarvam_api_key)


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    settings.upload_dir.mkdir(parents=True, exist_ok=True)
    settings.model_path.parent.mkdir(parents=True, exist_ok=True)
    return settings
