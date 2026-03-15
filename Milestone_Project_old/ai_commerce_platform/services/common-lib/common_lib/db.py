from pymongo import MongoClient

from .config import get_settings


def get_db():
    settings = get_settings()
    client = MongoClient(settings.mongo_uri)
    return client[settings.mongo_db]
