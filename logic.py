import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

# Initialize Client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Default Personality
system_context = "Act as a professional technical interviewer. Keep responses concise (max 2 sentences)."

def set_resume_context(resume_text):
    global system_context
    system_context = f"""
    You are a strict technical interviewer.
    Here is the candidate's resume: {resume_text}
    
    RULES:
    1. Listen to the candidate's audio answer.
    2. Ask follow-up questions based on their resume skills.
    3. Keep responses short and conversational.
    """
    print(f"✅ Brain Updated with Resume")

def get_gemini_response(history, user_audio_bytes):
    """
    Sends Audio directly to Gemini with AUTO-RETRY logic.
    """
    
    # 1. Prepare Audio Part (Generic MP3 format is safest)
    audio_part = types.Part.from_bytes(
        data=user_audio_bytes,
        mime_type="audio/mp3" 
    )

    # 2. Add to History
    history.append(
        types.Content(
            role="user",
            parts=[audio_part]
        )
    )

    # 3. Generate Response with Retry Loop
    # We try 3 times before giving up.
    for attempt in range(3):
        try:
            # "gemini-flash-latest" points to the stable 1.5 Flash model
            # This is usually much safer than the 2.0 Preview models
            response = client.models.generate_content(
                model="gemini-flash-latest", 
                contents=history,
                config=types.GenerateContentConfig(
                    system_instruction=system_context
                )
            )
            return response.text
            
        except Exception as e:
            # Check if it's the specific "Too Many Requests" error
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                print(f"⚠️ Quota hit. Waiting 5 seconds... (Attempt {attempt+1}/3)")
                time.sleep(5) # Wait and try again
            else:
                # If it's a different error, print it and crash gracefully
                print(f"❌ Gemini Crash: {e}")
                return "I'm having trouble connecting to my brain. Let's move to the next question."

    return "I am currently overloaded. Please try again in a moment."