import asyncio

from telegram.ext import Application, CommandHandler, MessageHandler, filters

from backend.core.config import get_settings
from backend.core.logging import configure_logging
from bot.commands.basic import about, help_command, history, language, predict_command, settings, start
from bot.handlers.messages import handle_error, handle_photo, handle_text, handle_voice


def build_application() -> Application:
    settings_obj = get_settings()
    if not settings_obj.telegram_bot_token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is missing. Add it to .env.")
    configure_logging(settings_obj.log_level)
    app = Application.builder().token(settings_obj.telegram_bot_token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("predict", predict_command))
    app.add_handler(CommandHandler("history", history))
    app.add_handler(CommandHandler("language", language))
    app.add_handler(CommandHandler("about", about))
    app.add_handler(CommandHandler("settings", settings))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_error_handler(handle_error)
    return app


async def main() -> None:
    app = build_application()
    await app.initialize()
    await app.start()
    await app.updater.start_polling(drop_pending_updates=True)
    try:
        await asyncio.Event().wait()
    finally:
        await app.updater.stop()
        await app.stop()
        await app.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
