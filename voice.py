import os
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from openai import OpenAI

load_dotenv()

# Initialize Clients
eleven_client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def transcribe_audio(audio_file):
    """
    Sends audio file to OpenAI Whisper and returns the text.
    """
    try:
        transcription = openai_client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file
        )
        return transcription.text
    except Exception as e:
        print(f"Transcription Error: {e}")
        return "I could not understand that."

def generate_speech(text):
    """
    Sends text to ElevenLabs (New V1 Syntax) and returns audio bytes.
    """
    try:
        # UPDATED: Use text_to_speech.convert instead of generate
        # Rachel's Voice ID: 21m00Tcm4TlvDq8ikWAM
        audio_generator = eleven_client.text_to_speech.convert(
            text=text,
            voice_id="21m00Tcm4TlvDq8ikWAM", 
            model_id="eleven_turbo_v2_5"
        )
        
        # Consumes the generator to create a single byte string
        return b"".join(audio_generator)
    
    except Exception as e:
        print(f"Speech Generation Error: {e}")
        return None
