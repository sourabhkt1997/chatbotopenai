import pymongo
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()
import os
mongourl=os.getenv("mongourl")
client = MongoClient(mongourl)
db = client.get_database()
