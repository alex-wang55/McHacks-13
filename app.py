from flask import Flask, request, jsonify, send_file, render_template
from database import get_database
from voice import transcribe_audio, generate_speech
from logic import get_gemini_response, set_resume_context
from pypdf import PdfReader
import io
import os

# --- FIX: Create the app variable FIRST ---
app = Flask(__name__)
db = get_database()

# Store chat history in memory
chat_history = []

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/upload-resume', methods=['POST'])
def upload_resume():
    if 'resume' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['resume']
    
    try:
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
            
        set_resume_context(text)
        return jsonify({"message": "Resume received."})
        
    except Exception as e:
        print(f"❌ PDF Error: {e}")
        return jsonify({"error": "Failed to read PDF"}), 500

@app.route('/api/process-audio', methods=['POST'])
def process_audio():
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    audio_file = request.files['audio']
    
    # 1. Transcribe
    user_text = transcribe_audio(audio_file)
    print(f"User said: {user_text}")

    # 2. AI Logic
    ai_text = get_gemini_response(chat_history, user_text)
    
    # Update History
    from google.genai import types
    chat_history.append(
        types.Content(
            role="model",
            parts=[types.Part.from_text(text=ai_text)]
        )
    )

    # 3. Save to Database
    if db is not None:
        db.interviews.insert_one({
            "user_said": user_text,
            "ai_said": ai_text
        })

    # 4. Speak
    audio_bytes = generate_speech(ai_text)
    
    if not audio_bytes:
        return jsonify({"error": "Failed to generate speech"}), 500

    return send_file(
        io.BytesIO(audio_bytes),
        mimetype="audio/mpeg"
    )

if __name__ == '__main__':
    app.run(debug=True, port=5000)
