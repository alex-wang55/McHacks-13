from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
import os
from dotenv import load_dotenv
import certifi

load_dotenv()

def get_database():
    connection_string = os.getenv("MONGO_URI")
    if not connection_string:
        print("⚠️ No MONGO_URI found. Running offline.")
        return None

    try:
        # Try to connect with a 5-second timeout
        client = MongoClient(
            connection_string, 
            serverSelectionTimeoutMS=5000,
            tlsCAFile=certifi.where()
        )
        
        # Quick test to see if it works
        client.admin.command('ping')
        print("✅ Connected to MongoDB!")
        return client.get_database("mchacks_db")

    except Exception as e:
        # If it fails, we catch the error and return None
        print("❌ DB Connection Failed (likely WiFi blocked). Running Offline.")
        return None