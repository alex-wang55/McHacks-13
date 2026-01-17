import os
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from openai import OpenAI

load_dotenv()
eleven_client = ElevenLabs(api_key=os.getenv("sk_c59d6728bd32e6f7f5a579e4d7377f9788b132928bf9ab0b"))
openai_client = OpenAI(api_key=os.getenv("AIzaSyBNdxBmKiFnjzImV0IciVO4RdClNiD5JqA"))

def get_transcript_from_turn(audio_file):
    """
    Called automatically when the frontend VAD detects the user is done.
    """
    transcript = openai_client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file
    )
    return transcript.text

def generate_interviewer_reply(text):
    """
    Generates ultra-low latency audio for the interviewer.
    """
    audio_stream = eleven_client.generate(
        text=text,
        voice="Rachel",
        model="eleven_flash_v2_5", # Flash is crucial for 'automatic' feel
        stream=True
    )
    return b"".join(audio_stream)