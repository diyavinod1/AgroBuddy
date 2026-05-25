import base64
from pathlib import Path
from uuid import uuid4

import httpx
from gtts import gTTS

from backend.core.config import Settings, get_settings
from backend.services.language import normalize_language


class SpeechService:
    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()

    async def speech_to_text(self, audio_path: str | Path, language: str = "en") -> str:
        if not self.settings.sarvam_enabled:
            return "Voice received. Please type the message if speech recognition is unavailable."
        headers = {"api-subscription-key": self.settings.sarvam_api_key}
        files = {"file": (Path(audio_path).name, Path(audio_path).read_bytes(), "audio/ogg")}
        data = {"language_code": self._sarvam_language(normalize_language(language))}
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(self.settings.sarvam_stt_url, headers=headers, files=files, data=data)
        if response.status_code >= 400:
            return "Voice received. Please type the message if speech recognition is unavailable."
        payload = response.json()
        return payload.get("transcript") or payload.get("text") or "I could not clearly hear the voice note."

    async def text_to_speech(self, text: str, language: str = "en") -> Path:
        language = normalize_language(language)
        if self.settings.sarvam_enabled:
            audio = await self._sarvam_tts(text, language)
            if audio:
                return audio
        path = self.settings.upload_dir / f"tts_{uuid4().hex}.mp3"
        tts = gTTS(text=text[:4500], lang=self._gtts_language(language), slow=False)
        tts.save(str(path))
        return path

    async def _sarvam_tts(self, text: str, language: str) -> Path | None:
        headers = {"api-subscription-key": self.settings.sarvam_api_key, "Content-Type": "application/json"}
        payload = {"inputs": [text[:4500]], "target_language_code": self._sarvam_language(language), "speaker": "meera"}
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(self.settings.sarvam_tts_url, headers=headers, json=payload)
        if response.status_code >= 400:
            return None
        data = response.json()
        audio_value = None
        if isinstance(data.get("audios"), list) and data["audios"]:
            audio_value = data["audios"][0]
        elif data.get("audio"):
            audio_value = data["audio"]
        if not audio_value:
            return None
        path = self.settings.upload_dir / f"sarvam_tts_{uuid4().hex}.wav"
        path.write_bytes(base64.b64decode(audio_value))
        return path

    def _sarvam_language(self, code: str) -> str:
        return {"en": "en-IN", "hi": "hi-IN", "ta": "ta-IN", "ml": "ml-IN", "kn": "kn-IN"}.get(code, "en-IN")

    def _gtts_language(self, code: str) -> str:
        return {"en": "en", "hi": "hi", "ta": "ta", "ml": "ml", "kn": "kn"}.get(code, "en")
