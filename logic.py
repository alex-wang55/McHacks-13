import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# --- FIX: Load secrets BEFORE doing anything else ---
load_dotenv()

# Now it is safe to get the key
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

system_context = "Act as a high-pressure technical interviewer. Ask one difficult question at a time. Wait for the user's response before asking the next question."

def set_resume_context(resume_text):
    global system_context
    system_context = f"""
    Act as a high-pressure technical interviewer. 
    Here is the candidate's resume context: 
    {resume_text}
    
    Instructions:
    1. Ask specific questions based on the skills and experience listed above.
    2. Do not just summarize the resume; test their deep knowledge of the tools they listed.
    3. Keep your responses concise (2-3 sentences max).
    """

def get_gemini_response(history, user_input):
    history.append(
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=user_input)]
        )
    )

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=history,
        config=types.GenerateContentConfig(
            system_instruction=system_context
        )
    )
    return response.text
