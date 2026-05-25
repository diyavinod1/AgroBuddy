from backend.database.repositories import UserRepository
from backend.services.language import normalize_language


class UserService:
    def __init__(self, repository: UserRepository | None = None) -> None:
        self.repository = repository or UserRepository()

    def ensure_user(self, telegram_user_id: int, name: str | None = None, username: str | None = None) -> dict:
        return self.repository.upsert_user(telegram_user_id, name, username)

    def get_user(self, telegram_user_id: int) -> dict | None:
        return self.repository.get_by_telegram_id(telegram_user_id)

    def set_language(self, telegram_user_id: int, language: str) -> dict:
        user = self.get_user(telegram_user_id)
        if user is None:
            user = self.ensure_user(telegram_user_id)
        return self.repository.set_language(telegram_user_id, normalize_language(language))
