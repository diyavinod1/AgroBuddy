# 🌱 AgroBuddy

### 🤖 Your AI Farming Buddy on Telegram (because plants deserve tech support too)

AgroBuddy is an AI-powered assistant that helps farmers understand their crops using **chat, images, and voice messages** — basically like a "doctor for plants", but without the waiting room.

If your plant looks sad 🌿 → AgroBuddy tries to figure out why.

If you're confused 🤔 → AgroBuddy explains like a patient farming friend.

If you're lazy to type 🎙️ → just speak.

---

## ⚡ What AgroBuddy actually does

- 🧠 Remembers your plants (yes, it has memory… better than some humans)
- 📸 Looks at crop images and tries to diagnose issues
- 💬 Gives farming advice like fertilizers, irrigation, and prevention tips
- 🎙️ Understands voice messages (because typing is hard in 2026)
- 🌍 Talks in multiple Indian languages
- 🗄️ Stores your chats so it doesn't "forget your chilli plant"
- ⚡ Uses AI to answer farming questions in real time

---

## 🧠 How it works (simple version)

AgroBuddy is basically a team of tiny digital brains working together:

- 💬 Telegram Bot → talks to users
- 🧠 AI Brain (OpenRouter LLMs) → answers questions
- 🗄️ Database (Supabase) → remembers conversations
- 📸 Vision module → checks plant images
- 🎤 Voice system → listens & speaks back

Think of it like:

> "ChatGPT + Plant Doctor + Memory + WhatsApp-like interface"

---

## 🛠️ Tech Stack (aka ingredients)

- Python 🐍 (because obviously)
- FastAPI ⚡
- Telegram Bot API 🤖
- OpenRouter (LLMs 🧠)
- Supabase 🗄️
- OpenCV 👀
- TensorFlow (optional… when it behaves)
- gTTS / Sarvam AI 🎙️
- Docker 🐳 (for pretending we are DevOps engineers)

---

## 📁 Project Structure

```
AgroBuddy/
├── backend/   # brain of the system 🧠
├── bot/       # talks to humans (important job)
├── ml/        # tries to understand plants 🌿
├── models/    # trained "plant wisdom"
├── scripts/   # training rituals
├── tests/     # where we hope nothing breaks
└── uploads/   # plant selfies 📸
```

---

## ⚙️ Setup (don't worry, it's not scary)

### 1. Clone it

```bash
git clone https://github.com/diyavinod1/AgroBuddy
cd AgroBuddy
```

### 2. Install dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Create `.env`

```env
TELEGRAM_BOT_TOKEN=your_token
LLM_API_KEY=your_key
LLM_MODEL=meta-llama/llama-3.1-8b-instruct
SUPABASE_URL=your_url
SUPABASE_KEY=your_key
SARVAM_API_KEY=your_key
JWT_SECRET=your_secret
```

### 4. Run it 🚀

```bash
# backend
python -m uvicorn backend.main:app --reload

# bot
python -m bot.bot
```

---

## 🌾 How to use AgroBuddy

Just talk to it like a confused farmer (or developer):

- `/start` → say hello
- Send 🌿 image → "what's wrong with my plant?"
- Send 💬 text → farming advice
- Send 🎙️ voice → because typing is overrated

---

## 🧪 Testing

```bash
pytest
ruff check .
```

---

## 🚀 Deployment note

This project is designed to run anywhere… except when Python versions decide to have a personality crisis.

⚠️ If deployment fails, it is usually:

- Python version mismatch 😭
- TensorFlow being dramatic 🤡
- Or the universe testing you

---

## 👥 Team AgroBuddy

- **Diya Vinod** — Team Lead (a.k.a. "why is this not working yet" person)
- **Sarulatha S** — ML & AI (teaches machines how to see plants)
- **Subin Raj P** — Backend & Bot (makes sure the bot actually replies instead of ghosting users)

---

## 🎯 Mission

To make farming advice:
- as easy as sending a WhatsApp message
- and slightly smarter than asking your neighbor.

---

## 🔮 Future Ideas (if we survive exams)

- 🌦️ Weather-based crop advice
- 🚁 Drone-based crop scanning
- 📊 Yield prediction
- 🏛️ Government scheme recommendations
- 📱 Offline farmer app

---

## 📌 Status

- 🟡 "Works perfectly on my machine" stage
- 🧪 Actively being improved
- ☕ Powered by late-night debugging sessions

---

## ❤️ Final Note

AgroBuddy is not just a project.
It's an attempt to make AI feel less like "AI"
and more like a helpful farming friend who never sleeps 🌱
