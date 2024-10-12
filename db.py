import os
from dotenv import load_dotenv
from pymongo import MongoClient
from models.user_model import User, UserInDB, Tags, UserType


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
        user_type=UserType.Student,
        tags=[Tags.Languages],
        academical_index="A"
    )
    db_instance = DB()
    # msg = db_instance.create_new_user(new_user)
    # print(msg)
    user = db_instance.get_user("user1")
    print(user)


        