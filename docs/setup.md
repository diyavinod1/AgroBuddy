# Setup Checklist

1. Install Python 3.11 and Docker.
2. Copy `.env.example` to `.env`.
3. Fill Telegram, SambaNova, Sarvam, Supabase, and JWT values.
4. Run `backend/database/schema.sql` in Supabase.
5. Run `pip install -r requirements.txt`.
6. Start API with `python -m uvicorn backend.main:app --reload`.
7. Start bot with `python -m bot.bot`.
8. Send `/start` to the bot.

