<<<<<<< HEAD
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def get_database():
    uri = os.environ.get("MONGO_URI")
    
    if not uri:
        print("❌ ERROR: MONGO_URI is missing from .env file!")
        return None

    try:
        client = MongoClient(uri)
        client.admin.command('ping')
        print("✅ SUCCESS: Connected to MongoDB!")
        return client['interview_db']
        
    except Exception as e:
        print(f"❌ CONNECTION FAILED: {e}")
        return None
=======
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def get_database():
    uri = os.environ.get("MONGO_URI")
    
    if not uri:
        print("❌ ERROR: MONGO_URI is missing from .env file!")
        return None

    try:
        client = MongoClient(uri)
        client.admin.command('ping')
        print("✅ SUCCESS: Connected to MongoDB!")
        return client['interview_db']
        
    except Exception as e:
        print(f"❌ CONNECTION FAILED: {e}")
        return None
>>>>>>> c9a6c9f69360d2ff917f3cc8192fa84ac13fdf7c
