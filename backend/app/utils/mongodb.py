from pymongo import MongoClient
import os

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "forum")

client = MongoClient(MONGO_URL)

def get_database():
    """
    Get a reference to the MongoDB forum database.
    """
    return client[MONGO_DB_NAME]
