# Methodology

AgroBuddy uses a modular architecture with independent layers for Telegram interaction, FastAPI services, Supabase persistence, computer vision, speech, and conversational AI.

Image workflow:

- Receive image from Telegram or API.
- Store the upload in `uploads/`.
- Decode and resize with OpenCV.
- Normalize pixels for TensorFlow inference.
- Run a Keras PlantVillage classifier when available.
- Use deterministic visual heuristics as a runnable fallback when no large model artifact is present.
- Map predicted class to symptoms, remedies, fertilizer suggestions, and prevention.
- Generate Grad-CAM overlays when a trained convolutional model is loaded.

Conversational workflow:

- Persist or load the Telegram user.
- Retrieve recent chat context from Supabase.
- Build a farmer-friendly SambaNova prompt.
- Generate a response in the selected language.
- Store the conversation.

Speech workflow:

- Download Telegram voice note.
- Transcribe with Sarvam speech-to-text.
- Generate AI response.
- Synthesize speech with Sarvam text-to-speech.
- Fall back to gTTS if Sarvam TTS is unavailable.

