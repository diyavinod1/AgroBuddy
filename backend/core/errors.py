from fastapi import HTTPException, status


class AgroBuddyError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class ExternalServiceError(AgroBuddyError):
    """Raised when a configured third-party AI or speech service fails."""


class DatabaseUnavailableError(AgroBuddyError):
    """Raised when Supabase credentials are missing or unavailable."""


def http_error(message: str, code: int = status.HTTP_400_BAD_REQUEST) -> HTTPException:
    return HTTPException(status_code=code, detail={"error": message})
