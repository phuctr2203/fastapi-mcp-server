from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["game_db"]
games_collection = db["games"]
games_collection.create_index([("title", 1)], unique=True)
