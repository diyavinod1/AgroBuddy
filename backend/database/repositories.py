from typing import Any

from backend.database.client import supabase_provider


class UserRepository:
    table = "users"

    def get_by_telegram_id(self, telegram_user_id: int) -> dict[str, Any] | None:
        response = (
            supabase_provider.client.table(self.table)
            .select("*")
            .eq("telegram_user_id", telegram_user_id)
            .limit(1)
            .execute()
        )
        return response.data[0] if response.data else None

    def upsert_user(self, telegram_user_id: int, name: str | None, username: str | None, language: str = "en") -> dict[str, Any]:
        existing = self.get_by_telegram_id(telegram_user_id)
        payload = {
            "telegram_user_id": telegram_user_id,
            "name": name,
            "username": username,
            "language": existing.get("language", language) if existing else language,
        }
        response = supabase_provider.client.table(self.table).upsert(payload, on_conflict="telegram_user_id").execute()
        return response.data[0]

    def set_language(self, telegram_user_id: int, language: str) -> dict[str, Any]:
        response = (
            supabase_provider.client.table(self.table)
            .update({"language": language})
            .eq("telegram_user_id", telegram_user_id)
            .execute()
        )
        return response.data[0]


class ChatHistoryRepository:
    table = "chat_history"

    def create(self, user_id: str, message: str, response: str) -> dict[str, Any]:
        result = supabase_provider.client.table(self.table).insert(
            {"user_id": user_id, "message": message, "response": response}
        ).execute()
        return result.data[0]

    def list_for_user(self, user_id: str, limit: int = 10) -> list[dict[str, Any]]:
        result = (
            supabase_provider.client.table(self.table)
            .select("*")
            .eq("user_id", user_id)
            .order("timestamp", desc=True)
            .limit(limit)
            .execute()
        )
        return result.data or []


class PredictionRepository:
    table = "predictions"

    def create(
        self,
        user_id: str,
        image_path: str,
        crop_name: str,
        disease_name: str,
        confidence: float,
        remedies: list[str],
        fertilizer: list[str],
        prevention: list[str],
    ) -> dict[str, Any]:
        result = supabase_provider.client.table(self.table).insert(
            {
                "user_id": user_id,
                "image_path": image_path,
                "crop_name": crop_name,
                "disease_name": disease_name,
                "confidence": confidence,
                "remedies": remedies,
                "fertilizer": fertilizer,
                "prevention": prevention,
            }
        ).execute()
        return result.data[0]

    def list_for_user(self, user_id: str, limit: int = 10) -> list[dict[str, Any]]:
        result = (
            supabase_provider.client.table(self.table)
            .select("*")
            .eq("user_id", user_id)
            .order("created_at", desc=True)
            .limit(limit)
            .execute()
        )
        return result.data or []
