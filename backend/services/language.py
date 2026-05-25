from ml.knowledge_base import LANGUAGE_NAMES, SUPPORTED_LANGUAGES


def normalize_language(language: str | None) -> str:
    if not language:
        return "en"
    code = language.lower().strip()
    aliases = {
        "english": "en",
        "hindi": "hi",
        "tamil": "ta",
        "malayalam": "ml",
        "kannada": "kn",
    }
    code = aliases.get(code, code)
    return code if code in SUPPORTED_LANGUAGES else "en"


def language_label(code: str) -> str:
    return LANGUAGE_NAMES.get(normalize_language(code), "English")
