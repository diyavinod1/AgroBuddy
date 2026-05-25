# API Reference

Swagger is available at `/docs` when the server is running.

Core endpoints:

- `GET /health`
- `POST /predict`
- `POST /chat`
- `POST /speech-to-text`
- `POST /text-to-speech`
- `GET /history/{telegram_user_id}`

All routes are async and return JSON except text-to-speech, which returns an audio file.

