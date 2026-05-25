# Architecture

AgroBuddy follows a service-oriented monolith structure suitable for research deployment and production hardening.

Layers:

- Telegram bot: user interaction, commands, media download, and response delivery.
- FastAPI backend: HTTP API for prediction, chat, speech, and history.
- Services: business logic for users, chat, predictions, speech, and history.
- Database: Supabase SDK repositories using a repository pattern.
- ML: preprocessing, model loading, inference, explainability, and disease knowledge.
- Deployment: Dockerfile, Docker Compose, and startup scripts.

Data flow:

1. Farmer sends a text, image, or voice note.
2. Telegram handler delegates to the appropriate service.
3. Services call Supabase, SambaNova, Sarvam, and ML modules.
4. Results are formatted into concise farmer-facing guidance.
5. History and predictions are persisted for context and auditability.

