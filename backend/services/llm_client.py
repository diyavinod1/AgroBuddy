from typing import Any

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

from backend.core.config import Settings, get_settings
from backend.core.errors import ExternalServiceError


class LLMClient:
    base_url = "https://openrouter.ai/api/v1/chat/completions"

    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=6))
    async def chat(self, messages: list[dict[str, str]], temperature: float = 0.35) -> str:
        if not self.settings.llm_enabled:
            return self._local_response(messages[-1]["content"])
        headers = {
            "Authorization": f"Bearer {self.settings.llm_api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:8000",
            "X-Title": "AgroBuddy"
        }
        payload: dict[str, Any] = {
            "model": self.settings.llm_model,
            "messages": messages,
            "temperature": temperature,
            "top_p": 0.9,
        }
        async with httpx.AsyncClient(timeout=45) as client:
            response = await client.post(self.base_url, headers=headers, json=payload)
        if response.status_code >= 400:
            raise ExternalServiceError(f"LLM API failed: {response.text[:300]}")
        data = response.json()
        return data["choices"][0]["message"]["content"].strip()

    def _local_response(self, message: str) -> str:
        lowered = message.lower()
        if "fertil" in lowered or "npk" in lowered:
            return (
                "Use fertilizer based on a soil test. As a safe general rule, apply compost or farmyard manure, "
                "use balanced NPK in split doses, and avoid excess nitrogen if disease symptoms are visible."
            )
        if "water" in lowered or "irrig" in lowered:
            return (
                "Water near the root zone early in the morning. Keep soil moist but not waterlogged, and reduce "
                "overhead watering because wet leaves increase fungal disease risk."
            )
        return (
            "I can help with crop disease, irrigation, fertilizer, and prevention advice. Send a clear leaf photo "
            "for disease prediction, or describe your crop, symptoms, location, and recent weather."
        )
