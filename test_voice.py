from voice import generate_speech

print("Testing ElevenLabs...")
audio = generate_speech("Hello, this is a test of the emergency broadcast system.")

if audio:
    with open("test_output.mp3", "wb") as f:
        f.write(audio)
    print("✅ Success! Check your folder for 'test_output.mp3'")
else:
    print("❌ Failed. Check your API Key.")