from pymongo import MongoClient

from settings import settings


client = MongoClient(settings.db_host, 27017)

db = client[settings.db_name]
collection = db[settings.db_collection]
    
