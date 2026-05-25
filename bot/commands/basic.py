from telegram import Update
from telegram.ext import ContextTypes

from backend.services.history_service import HistoryService
from backend.services.language import normalize_language
from backend.services.user_service import UserService
from bot.services.formatters import help_message, language_menu, settings_message


async def start(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    if user is None or update.message is None:
        return
    UserService().ensure_user(user.id, user.full_name, user.username)
    await update.message.reply_text(
        "Welcome to AgroBuddy. Send a crop photo, voice note, or farming question and I will help with practical advice."
    )


async def help_command(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:
        await update.message.reply_text(help_message())


async def predict_command(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:
        await update.message.reply_text("Please upload a clear crop leaf photo. I will analyze disease, remedies, fertilizer, and prevention.")


async def about(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:
        await update.message.reply_text(
            "AgroBuddy is an AI-powered farmer assistance Telegram bot using computer vision, conversational AI, speech, and Supabase history."
        )


async def language(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:
        await update.message.reply_text(language_menu())


async def settings(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.effective_user:
        return
    user = UserService().get_user(update.effective_user.id)
    lang = normalize_language(user.get("language") if user else "en")
    await update.message.reply_text(settings_message(lang))


async def history(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.effective_user:
        return
    data = HistoryService().history(update.effective_user.id, limit=5)
    chats = data["chat_history"]
    predictions = data["predictions"]
    lines = ["Recent AgroBuddy history:"]
    if not chats and not predictions:
        lines.append("No history yet. Send a question or crop image to begin.")
    for item in predictions[:3]:
        lines.append(f"Image: {item['crop_name']} - {item['disease_name']} ({item['confidence'] * 100:.1f}%)")
    for item in chats[:3]:
        lines.append(f"Q: {item['message'][:80]}")
        lines.append(f"A: {item['response'][:120]}")
    await update.message.reply_text("\n".join(lines))
