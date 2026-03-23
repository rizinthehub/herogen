from pymongo import MongoClient
from datetime import datetime
import os

def get_db():
    """Connect to MongoDB Atlas. Returns None if not configured."""
    uri = os.getenv("MONGODB_URI")
    
    if not uri:
        print("No MONGODB_URI found in .env!")
        return None
    
    try:
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        client.server_info()  # Test the connection
        return client["herogen"]
    except Exception as e:
        print(f"MongoDB connection failed: {e}")
        return None

def save_story(user_id, child_name, age, moral, story_data, image_urls):
    """Save a generated story to MongoDB."""
    db = get_db()
    if not db:
        return None
    
    doc = {
        "user_id": user_id,
        "child_name": child_name,
        "age": age,
        "moral": moral,
        "created_at": datetime.utcnow(),
        "status": "completed",
        "content": story_data,
        "image_urls": image_urls,
    }
    
    try:
        result = db.stories.insert_one(doc)
        return str(result.inserted_id)
    except Exception as e:
        print(f"Failed to save story: {e}")
        return None

def get_user_stories(user_id):
    """Retrieve all stories for a user."""
    db = get_db()
    if not db:
        return []
    
    try:
        return list(db.stories.find(
            {"user_id": user_id}).sort("created_at", -1))
    except:
        return []