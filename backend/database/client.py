from supabase import Client, create_client

from backend.core.config import Settings, get_settings
from backend.core.errors import DatabaseUnavailableError


class SupabaseProvider:
    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()
        self._client: Client | None = None

    @property
    def client(self) -> Client:
        if not self.settings.supabase_enabled:
            raise DatabaseUnavailableError("Supabase is not configured. Fill SUPABASE_URL and SUPABASE_KEY in .env.")
        if self._client is None:
            self._client = create_client(self.settings.supabase_url, self.settings.supabase_key)
        return self._client


supabase_provider = SupabaseProvider()
