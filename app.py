from flask import Flask, request, jsonify, render_template
from database import get_database
from voice import generate_speech
from logic import get_gemini_response, set_resume_context
from pypdf import PdfReader
import base64

app = Flask(__name__)

# Try to connect to DB, but don't crash if it fails
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
        return jsonify({"message": "Resume processed."})
        
    except Exception as e:
        print(f"❌ PDF Error: {e}")
        return jsonify({"error": "Failed to read PDF"}), 500

@app.route('/api/process-audio', methods=['POST'])
def process_audio():
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    # Get raw audio bytes
    audio_file = request.files['audio']
    audio_bytes = audio_file.read()
    
    # Send to Gemini (No transcription needed)
    user_text_display = "(Audio Message)" 
    
    try:
        ai_text = get_gemini_response(chat_history, audio_bytes)
    except Exception as e:
        print(f"❌ Gemini Error: {e}")
        return jsonify({"error": str(e)}), 500
    
    # Update History
    from google.genai import types
    chat_history.append(types.Content(role="model", parts=[types.Part.from_text(text=ai_text)]))

    # Save to MongoDB if DB is connected
    if db is not None:
        try:
            db.interviews.insert_one({
                "type": "audio",
                "ai_response": ai_text
            })
        except:
            pass # Ignore DB errors

    # Generate Speech
    audio_response_bytes = generate_speech(ai_text)
    
    if not audio_response_bytes:
        return jsonify({"error": "Failed to generate speech"}), 500

    audio_base64 = base64.b64encode(audio_response_bytes).decode('utf-8')

    return jsonify({
        "user_text": user_text_display,
        "ai_text": ai_text,
        "audio_data": audio_base64
    })

# makes the server start 
if __name__ == '__main__':
    print("🚀 Starting PrepPal Server...")
    # debug=False is safer for Python 3.14
    app.run(debug=False, port=5000)
