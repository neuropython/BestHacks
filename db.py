from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from models.user_model import User, UserInDB
import bcrypt
from http import HTTPStatus

# Load environment variables
load_dotenv()

PASSWORD = os.getenv("password")
USERNAME = os.getenv("user") 

MONGO_URI = f"mongodb+srv://{USERNAME}:{PASSWORD}@hackyeahbackend.ai51i.mongodb.net/?retryWrites=true&w=majority&appName=HackYeahBackend"

# FastAPI app instance
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

    def create_new_user(self, user: UserInDB):
        if self.db['Users'].find_one({"username": user.username}):
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="User already exists")
        if self.db['Users'].find_one({"email": user.email}):
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Email already exists")
        result = self.db['Users'].insert_one(user.dict())
        if result.inserted_id:
            return {"message": "User created successfully", "status_code": HTTPStatus.CREATED}
        else:
            raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Error creating user")

    def get_user(self, username: str):
        user = self.db['Users'].find_one({"username": username})
        if user:
            return User(**user)
        else:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
    
    def get_user_id(self, user_id: str):
        user = self.db['Users'].find_one({"id": user_id})
        if user:
            return User(**user)
        else:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
    
    def change_profile_picture(self, user_id: str, profile_picture: str):
        result = self.db['Users'].update_one({"id": user_id}, {"$set": {"profile_picture": profile_picture}})
        if result.modified_count:
            return {"message": "Profile picture updated successfully"}
        else:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Error updating profile picture")

    def validate_user(self, username: str, password: str):
        user = self.db['Users'].find_one({"username": username})
        if not user:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
        password_in_db = user["password"]
        if bcrypt.checkpw(password.encode('utf-8'), password_in_db.encode('utf-8')):
            return {"message": "User validated successfully"}
        else:
            raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid password")
