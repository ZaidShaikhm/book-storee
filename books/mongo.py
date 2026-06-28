# books/mongo.py
# All MongoDB Atlas connection logic lives here.
# Views import get_col() to get a collection handle.

from pymongo import MongoClient
from django.conf import settings

_client = None

def get_db():
    global _client
    if _client is None:
        _client = MongoClient(settings.MONGO_URI)
    return _client[settings.MONGO_DB]

def get_col(name):
    return get_db()[name]
