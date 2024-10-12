import os
from dotenv import load_dotenv
from pymongo import MongoClient
from fastapi import FastAPI

load_dotenv()
PASSWORD = os.getenv("password")
USERNAME = os.getenv("user") 

MONGO_URI = f"mongodb+srv://{USERNAME}:{PASSWORD}@hackyeahbackend.ai51i.mongodb.net/?retryWrites=true&w=majority&appName=HackYeahBackend"


app = FastAPI()

class DB:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DB, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        self.client = MongoClient(MONGO_URI)
        self.db = self.client['BestHacks']

db = DB()
