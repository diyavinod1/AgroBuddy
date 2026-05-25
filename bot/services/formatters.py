from backend.models.domain import PredictionResult
from backend.services.language import language_label


def prediction_message(result: PredictionResult) -> str:
    return (
        f"Crop: {result.crop_name.title()}\n"
        f"Disease: {result.disease_name}\n"
        f"Confidence: {result.confidence * 100:.1f}%\n\n"
        f"Symptoms:\n{_bullets(result.symptoms)}\n\n"
        f"Remedies:\n{_bullets(result.remedies)}\n\n"
        f"Fertilizer suggestions:\n{_bullets(result.fertilizer)}\n\n"
        f"Prevention:\n{_bullets(result.prevention)}"
    )


def help_message() -> str:
    return (
        "AgroBuddy commands:\n"
        "/start - Register and begin\n"
        "/predict - Send a crop leaf photo\n"
        "/history - View recent chats and predictions\n"
        "/language - Change language\n"
        "/settings - View current settings\n"
        "/about - About AgroBuddy\n"
        "/help - Show this help\n\n"
        "You can also send a text question, crop image, or voice note directly."
    )


def language_menu() -> str:
    return (
        "Choose a language by sending one of these:\n"
        "en - English\n"
        "hi - Hindi\n"
        "ta - Tamil\n"
        "ml - Malayalam\n"
        "kn - Kannada"
    )


def settings_message(language: str) -> str:
    return f"Current language: {language_label(language)} ({language})"


def _bullets(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)
