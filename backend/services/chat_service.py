from backend.database.repositories import ChatHistoryRepository
from backend.services.language import language_label, normalize_language
from backend.services.llm_client import LLMClient
from backend.services.user_service import UserService


class ChatService:
    def __init__(
        self,
        sambanova: LLMClient | None = None,
        users: UserService | None = None,
        history: ChatHistoryRepository | None = None,
    ) -> None:
        
        self.sambanova = sambanova or LLMClient()
        self.users = users or UserService()
        self.history = history or ChatHistoryRepository()

    async def reply(self, telegram_user_id: int, message: str, language: str | None = None) -> tuple[str, str]:
        user = self.users.get_user(telegram_user_id) or self.users.ensure_user(telegram_user_id)
        lang = normalize_language(language or user.get("language"))
        recent = self.history.list_for_user(user["id"], limit=6)
        messages = [
            {
                "role": "system",
                "content": (
                    "You are AgroBuddy, a practical AI farming assistant for small farmers. "
                    f"Reply in {language_label(lang)}. Use simple words, short steps, and field-ready advice. "
                    "Ask for crop, location, stage, weather, and photo only when needed. Never recommend unsafe chemical use; "
                    "tell farmers to follow local agricultural officer guidance and product labels."
                ),
            }
        ]
        for item in reversed(recent):
            messages.append({"role": "user", "content": item["message"]})
            messages.append({"role": "assistant", "content": item["response"]})
        messages.append({"role": "user", "content": message})
        response = await self.sambanova.chat(messages)
        self.history.create(user["id"], message, response)
        return response, lang
