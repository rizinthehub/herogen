from pymongo import MongoClient
from datetime import datetime
import os
import copy


def get_db():
    """Connect to MongoDB Atlas. Returns None if not configured."""
    uri = os.getenv("MONGODB_URI")
    if not uri:
        return None
    try:
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        client.server_info()
        return client["herogen"]
    except Exception as e:
        print(f"MongoDB connection failed: {e}")
        return None


def _make_serializable(obj):
    """Recursively convert any non-serializable types to strings."""
    if isinstance(obj, dict):
        return {str(k): _make_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [_make_serializable(item) for item in obj]
    elif isinstance(obj, (str, int, float, bool)):
        return obj
    elif obj is None:
        return obj
    else:
        return str(obj)


def save_story(user_id, child_name, age, moral, story_data, image_urls):
    """Save a generated story to MongoDB."""
    db = get_db()
    if not db:
        return None

    # Deep copy and sanitize to prevent type inference errors
    clean_story = _make_serializable(copy.deepcopy(story_data))
    clean_images = [str(url) if url else "" for url in image_urls]

    doc = {
        "user_id": str(user_id),
        "child_name": str(child_name),
        "age": int(age),
        "moral": str(moral),
        "created_at": datetime.utcnow(),
        "status": "completed",
        "content": clean_story,
        "image_urls": clean_images,
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
        return list(db.stories.find({"user_id": user_id}).sort("created_at", -1))
    except Exception:
        return []