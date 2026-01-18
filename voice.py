import os
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs

load_dotenv()

eleven_client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

def generate_speech(text):
    try:
        audio_generator = eleven_client.text_to_speech.convert(
            text=text,
            voice_id="21m00Tcm4TlvDq8ikWAM", 
            model_id="eleven_turbo_v2_5"
        )
        return b"".join(audio_generator)
    except Exception as e:
        print(f"❌ Speech Generation Error: {e}")
        return None