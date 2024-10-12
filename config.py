from dotenv import load_dotenv
import os
from pymongo import MongoClient

class ConnecttoDB:
    def __init__(self):
        load_dotenv()

        PASSWORD = os.getenv("password")
        USERNAME = os.getenv("user") 

        self.MONGO_URI = f"mongodb+srv://{USERNAME}:{PASSWORD}@hackyeahbackend.ai51i.mongodb.net/?retryWrites=true&w=majority&appName=HackYeahBackend"
    
    def connect(self):
        self.client = MongoClient(self.MONGO_URI)
        self.db = self.client['BestHacks']
        return self.db
        
