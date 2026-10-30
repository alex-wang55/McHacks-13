# PrepPal AI

A voice mock interviewer, built at McHacks 13 (January 2026) with [alanna24](https://github.com/alanna24) and [mattyc1](https://github.com/mattyc1).

Upload your resume, press the mic and answer out loud. An AI interviewer asks follow-up questions about the skills on your resume and says them back to you.

## How it works

- **Your resume is the context.** The PDF is read with pypdf and its text goes into Gemini's system instruction, so the questions are about your actual experience.
- **Gemini listens to the audio directly.** The browser records your answer and the server sends the raw audio to Gemini along with the conversation so far. There's no separate speech-to-text step; the browser's Web Speech API only shows your words in the chat.
- **ElevenLabs speaks the reply.** Gemini's answer is turned into speech with ElevenLabs and played back in the browser.
- **Rate limits don't crash it.** Gemini calls retry up to 3 times on a 429, and if they still fail the interviewer says so and moves on.
- **MongoDB is optional.** If `MONGO_URI` is set, the interviewer's replies are logged to MongoDB. Without it, or on a network that blocks it, the app runs offline.

## Stack

Flask, Gemini API (`google-genai`), ElevenLabs, pypdf, MongoDB (pymongo), and a plain HTML/CSS/JS front end.

## Running it locally

```bash
python -m venv venv
./venv/Scripts/activate   # Windows; use `source venv/bin/activate` on macOS/Linux
pip install -r requirements.txt
```

Create a `.env` file in the repo root:

```
GEMINI_API_KEY=your-gemini-key
ELEVENLABS_API_KEY=your-elevenlabs-key
MONGO_URI=your-mongodb-uri   # optional
```

Then start the server:

```bash
python app.py
```

Open http://127.0.0.1:5000, upload a resume PDF and allow microphone access. Chrome works best, since it supports both recording and live speech recognition.

`python test_voice.py` checks your ElevenLabs key by saving a short clip to `test_output.mp3`.

The conversation is kept in the server's memory, so restart the server to start a new interview.
