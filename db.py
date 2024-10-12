import os
from dotenv import load_dotenv
from pymongo import MongoClient
from models.user_model import User, UserInDB, Tags, UserType
import bcrypt


load_dotenv()

PASSWORD = os.getenv("password")
USERNAME = os.getenv("user") 

MONGO_URI = f"mongodb+srv://{USERNAME}:{PASSWORD}@hackyeahbackend.ai51i.mongodb.net/?retryWrites=true&w=majority&appName=HackYeahBackend"

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
            return {"message": "User already exists"}
        if self.db['Users'].find_one({"email": user.email}):
            return {"message": "Email already exists"}
        result = self.db['Users'].insert_one(user.dict())
        if result.inserted_id:
            return {"message": "User created successfully"}
        else:
            return {"message": "Error creating user"}

    def get_user(self, username: str):
        user = self.db['Users'].find_one({"username": username})
        if user:
            return User(**user)
        else:
            return {"message": "User not found"}
    
    def get_user_id(self, user_id: str):
        user = self.db['Users'].find_one({"id": user_id})
        if user:
            return User(**user)
        else:
            return {"message": "User not found"}
    
    def change_profile_picture(self, user_id: str, profile_picture: str):
        result = self.db['Users'].update_one({"id": user_id}, {"$set": {"profile_picture": profile_picture}})
        if result.modified_count:
            return {"message": "Profile picture updated successfully"}
        else:
            return {"message": "Error updating profile picture"}

    def validate_user(self, username: str, password: str):
        user = self.db['Users'].find_one({"username": username})
        password_in_db = user["password"]
        return bcrypt.checkpw(password.encode('utf-8'), password_in_db.encode('utf-8'))
        
                
if __name__ == "__main__":
    db = DB()
    new_user = UserInDB(
        name="John",
        second_name="Doe",
        bio="This is a bio",
        email="user@example.com",
        username="user1",
        password="password123",
        profile_picture="profile.jpg",
        how_many_requests=0,
        user_type='Student',
        tags=['Languages'],
        academical_index="A"
    )
    db_instance = DB()
    # msg = db_instance.create_new_user(new_user)
    # print(msg)
    user = db_instance.get_user("user1")
    # print(user.id)
    user = db_instance.get_user_id(user.id)
    # print(user.username)
    msg = db_instance.change_profile_picture(user.id, "new_profile.jpg")
    # print(msg)
    msg = db_instance.validate_user("user1", "password123")
    # print(msg)