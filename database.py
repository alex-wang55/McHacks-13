import os
from pymongo import MongoClient
from dotenv import load_dotenv

# 1. Load the secrets from your .env file
load_dotenv()

def get_database():
    # 2. Get the connection string (URI) you just pasted
    uri = os.environ.get("MONGO_URI")
    
    if not uri:
        print("❌ ERROR: MONGO_URI is missing from .env file!")
        return None

    try:
        # 3. Connect to the cloud
        client = MongoClient(uri)
        
        # 4. Test the connection by 'pinging' the server
        client.admin.command('ping')
        print("✅ SUCCESS: Connected to MongoDB!")
        return client['interview_db']
        
    except Exception as e:
        print(f"❌ CONNECTION FAILED: {e}")
        return None

# Test block: This runs only when you type 'python database.py'
if __name__ == "__main__":
    db = get_database()