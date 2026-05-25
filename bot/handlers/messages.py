from pathlib import Path
from uuid import uuid4

from telegram import Update
from telegram.ext import ContextTypes

from backend.core.config import get_settings
from backend.services.chat_service import ChatService
from backend.services.language import SUPPORTED_LANGUAGES, normalize_language
from backend.services.prediction_service import PredictionService
from backend.services.speech_service import SpeechService
from backend.services.user_service import UserService
from bot.services.formatters import prediction_message

import logging

async def handle_text(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message is None or update.effective_user is None or update.message.text is None:
        return
    text = update.message.text.strip()
    user_service = UserService()
    user = user_service.ensure_user(update.effective_user.id, update.effective_user.full_name, update.effective_user.username)
    if text.lower() in SUPPORTED_LANGUAGES:
        updated = user_service.set_language(update.effective_user.id, text.lower())
        await update.message.reply_text(f"Language updated to {updated['language']}.")
        return
    await update.message.chat.send_action("typing")
    response, _ = await ChatService().reply(update.effective_user.id, text, user.get("language"))
    await update.message.reply_text(response[:3900])


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message is None or update.effective_user is None or not update.message.photo:
        return
    UserService().ensure_user(update.effective_user.id, update.effective_user.full_name, update.effective_user.username)
    await update.message.reply_text("Analyzing the crop image now...")
    photo = update.message.photo[-1]
    file = await context.bot.get_file(photo.file_id)
    path = get_settings().upload_dir / f"telegram_leaf_{uuid4().hex}.jpg"
    await file.download_to_drive(custom_path=path)
    result = PredictionService().predict_for_user(update.effective_user.id, path)
    user = UserService().get_user(update.effective_user.id) or {}
    language = normalize_language(user.get("language"))
    message = prediction_message(result)
    if language != "en":
        message, _ = await ChatService().reply(
            update.effective_user.id,
            "Translate this crop diagnosis into the farmer's selected language while keeping the same sections and practical meaning:\n\n"
            + message,
            language,
        )
    await update.message.reply_text(message[:3900])
    if result.explanation_path and Path(result.explanation_path).exists():
        await update.message.reply_photo(photo=open(result.explanation_path, "rb"), caption="Grad-CAM disease attention map")


async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message is None or update.effective_user is None or update.message.voice is None:
        return
    user_service = UserService()
    user = user_service.ensure_user(update.effective_user.id, update.effective_user.full_name, update.effective_user.username)
    language = normalize_language(user.get("language"))
    await update.message.reply_text("Listening to your voice note...")
    voice_file = await context.bot.get_file(update.message.voice.file_id)
    path = get_settings().upload_dir / f"telegram_voice_{uuid4().hex}.ogg"
    await voice_file.download_to_drive(custom_path=path)
    speech = SpeechService()
    transcript = await speech.speech_to_text(path, language)
    response, lang = await ChatService().reply(update.effective_user.id, transcript, language)
    await update.message.reply_text(f"You said: {transcript}\n\n{response[:3400]}")
    audio_path = await speech.text_to_speech(response, lang)
    await update.message.reply_voice(voice=open(audio_path, "rb"))


async def handle_error(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    if isinstance(update, Update) and update.effective_message:
        await update.effective_message.reply_text(
            "Something went wrong while processing this request. Please check configuration and try again."
        )
    # context.application.logger.exception("Telegram handler failed", exc_info=context.error)
    logging.exception("Telegram handler failed", exc_info=context.error)
