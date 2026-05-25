from backend.database.repositories import ChatHistoryRepository, PredictionRepository
from backend.services.user_service import UserService


class HistoryService:
    def __init__(
        self,
        users: UserService | None = None,
        chats: ChatHistoryRepository | None = None,
        predictions: PredictionRepository | None = None,
    ) -> None:
        self.users = users or UserService()
        self.chats = chats or ChatHistoryRepository()
        self.predictions = predictions or PredictionRepository()

    def history(self, telegram_user_id: int, limit: int = 10) -> dict[str, list[dict]]:
        user = self.users.get_user(telegram_user_id)
        if user is None:
            return {"chat_history": [], "predictions": []}
        return {
            "chat_history": self.chats.list_for_user(user["id"], limit=limit),
            "predictions": self.predictions.list_for_user(user["id"], limit=limit),
        }
