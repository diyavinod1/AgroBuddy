# AgroBuddy

AI-Powered Farmer Assistance Telegram Bot Using Computer Vision and Conversational AI.

AgroBuddy is a production-ready Python project for a Telegram farming assistant. Farmers can send crop photos, voice notes, or text questions and receive disease prediction, remedies, fertilizer suggestions, prevention steps, and conversational guidance in English, Hindi, Tamil, Malayalam, and Kannada.

## Features

- Telegram bot commands: `/start`, `/help`, `/predict`, `/history`, `/language`, `/about`, `/settings`
- FastAPI backend with Swagger docs at `http://localhost:8000/docs`
- Crop image preprocessing with OpenCV
- TensorFlow/Keras model loading for PlantVillage transfer-learning classifiers
- Runnable heuristic fallback when no large model artifact is present
- Grad-CAM explainability when a trained CNN model is loaded
- SambaNova conversational AI integration
- Sarvam speech-to-text and text-to-speech integration
- gTTS fallback for speech output
- Supabase persistence for users, chat history, language, and predictions
- Docker and Docker Compose deployment

## Project Structure

```text
AgroBuddy/
├── backend/
│   ├── api/
│   ├── core/
│   ├── services/
│   ├── models/
│   ├── schemas/
│   ├── database/
│   └── main.py
├── bot/
│   ├── handlers/
│   ├── commands/
│   ├── services/
│   └── bot.py
├── ml/
│   ├── model_loader/
│   ├── inference/
│   ├── preprocessing/
│   └── explainability/
├── research/
├── docs/
├── tests/
├── uploads/
├── models/
├── scripts/
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## 1. Create API Keys

### Telegram

1. Open Telegram and message `@BotFather`.
2. Send `/newbot`.
3. Choose a bot name and username.
4. Copy the bot token into `.env` as `TELEGRAM_BOT_TOKEN`.

### Supabase

1. Create a project at Supabase.
2. Open SQL Editor.
3. Copy and run the SQL from `backend/database/schema.sql`.
4. Open Project Settings > API.
5. Copy Project URL to `SUPABASE_URL`.
6. Copy the service role key to `SUPABASE_KEY`. AgroBuddy runs server-side, so this key must stay only in `.env` on your trusted server.

### SambaNova

1. Create a SambaNova account.
2. Generate an API key.
3. Add it to `.env` as `SAMBANOVA_API_KEY`.

### Sarvam

1. Create a Sarvam AI account.
2. Generate an API key.
3. Add it to `.env` as `SARVAM_API_KEY`.

## 2. Configure Environment

```bash
cp .env.example .env
```

Edit `.env`:

```env
TELEGRAM_BOT_TOKEN=your_telegram_token
SAMBANOVA_API_KEY=your_sambanova_key
SARVAM_API_KEY=your_sarvam_key
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_key
JWT_SECRET=change_this_to_a_long_random_secret
```

The bot and API run after filling only those required values. Optional model variables already have defaults.

## 3. Local Installation

Python 3.11 is recommended.

```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

Run the API:

```bash
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

Run the Telegram bot in another terminal:

```bash
source .venv/bin/activate
python -m bot.bot
```

Open Swagger:

```text
http://localhost:8000/docs
```

## 4. Docker Setup

```bash
docker compose up --build
```

API:

```text
http://localhost:8000/health
```

Swagger:

```text
http://localhost:8000/docs
```

## 5. Model Setup

AgroBuddy runs immediately with a deterministic image-analysis fallback. For research or production accuracy, train a PlantVillage transfer-learning classifier:

```bash
python scripts/train_plantvillage.py \
  --data-dir /path/to/PlantVillage \
  --output-model models/plant_disease_model.keras \
  --output-labels models/labels.json \
  --epochs 8
```

The dataset directory must contain one folder per class, for example:

```text
PlantVillage/
├── Tomato___Late_blight/
├── Tomato___Early_blight/
├── Potato___Late_blight/
└── Corn___Common_rust/
```

After training, restart the API and bot. AgroBuddy automatically loads `models/plant_disease_model.keras` and `models/labels.json`.

## 6. API Usage

Health:

```bash
curl http://localhost:8000/health
```

Chat:

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"telegram_user_id":12345,"message":"How often should I irrigate tomato?","language":"en"}'
```

Predict:

```bash
curl -X POST http://localhost:8000/predict \
  -F "telegram_user_id=12345" \
  -F "image=@leaf.jpg"
```

History:

```bash
curl http://localhost:8000/history/12345
```

Speech-to-text:

```bash
curl -X POST http://localhost:8000/speech-to-text \
  -F "language=en" \
  -F "audio=@voice.ogg"
```

Text-to-speech:

```bash
curl -X POST http://localhost:8000/text-to-speech \
  -F "language=en" \
  -F "text=Water near the roots early in the morning." \
  --output reply.mp3
```

## 7. Telegram Usage

Start the bot on Telegram:

```text
/start
```

Then try:

```text
/language
hi
```

Send a leaf photo for disease prediction, or ask:

```text
What fertilizer should I use for tomato flowering stage?
```

Send a voice note to receive both text and voice replies.

## 8. Testing

```bash
pytest
```

Run linting:

```bash
ruff check .
```

## 9. Deployment Guide

For a VM deployment:

```bash
git clone <your-repo-url> AgroBuddy
cd AgroBuddy
cp .env.example .env
nano .env
docker compose up --build -d
```

Confirm:

```bash
docker compose ps
curl http://localhost:8000/health
```

For production:

- Use Supabase service role key only on trusted servers.
- Put the API behind HTTPS with Nginx, Caddy, or a cloud load balancer.
- Mount persistent volumes for `uploads/` and `models/`.
- Keep `.env` out of Git.
- Rotate API keys periodically.

## 10. Troubleshooting

`TELEGRAM_BOT_TOKEN is missing`

- Fill `.env` and restart the bot.

`Supabase is not configured`

- Fill `SUPABASE_URL` and `SUPABASE_KEY`.
- Run `backend/database/schema.sql` in Supabase SQL Editor.

`SambaNova API failed`

- Check `SAMBANOVA_API_KEY`.
- Confirm `SAMBANOVA_MODEL` is available in your account.

`gTTS failed`

- gTTS requires internet access. Use Sarvam TTS in production for a stronger speech path.

`TensorFlow install is slow`

- TensorFlow is large. Use Docker for the simplest repeatable setup.

## Security Notes

- Do not commit `.env`.
- Keep Supabase Row Level Security enabled.
- Prefer a service role key only in secure backend environments.
- Validate uploaded file types before storage. AgroBuddy already checks image content type in the API.
