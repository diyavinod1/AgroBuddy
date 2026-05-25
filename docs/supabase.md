# Supabase Setup

Run `backend/database/schema.sql` in the Supabase SQL Editor. Use the Supabase service role key in `.env` because AgroBuddy is a trusted server-side application.

Tables:

- `users`: Telegram identity and selected language.
- `chat_history`: user messages and assistant responses.
- `predictions`: crop disease prediction records.

Indexes are included for Telegram lookup and recent-history queries.
