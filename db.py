from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from models.user_model import User, UserInDB, Tags
from models.annoucement_model import Annoucement
from models.note_model import Note
import bcrypt
from http import HTTPStatus

# Load environment variables
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
        
    def add_annoucement(self, annoucement: Annoucement):
        if annoucement.owner_id:
            user = self.db['Users'].find_one({"id": annoucement.owner_id})
            if not user:
                raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
        result = self.db['Annoucements'].insert_one(annoucement.dict())
        if result.inserted_id:
            self.db['Users'].update_one({"id": annoucement.owner_id}, {"$inc": {"how_many_requests": 1}})
            return {"message": "Annoucement added successfully", "status_code": HTTPStatus.CREATED}
        else:
            raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Error adding annoucement")
    
    def get_all_annoucements(self):
        annoucements = self.db['Annoucements'].find()
        return [Annoucement(**annoucement) for annoucement in annoucements]

    def get_annoucement(self, annoucement_id: str):
        annoucement = self.db['Annoucements'].find_one({"id": annoucement_id})
        if annoucement:
            self.db['Annoucements'].update_one({"id": annoucement_id}, {"$inc": {"views": 1}})
            return Annoucement(**annoucement)
        else:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Annoucement not found")

    def get_annoucement_owner(self, owner: str):
        annoucements = self.db['Annoucements'].find({"owner": owner})
        return [Annoucement(**annoucement) for annoucement in annoucements]  

    def get_all_tags(self):
        return [tag.value for tag in Tags]
    
    def send_note(self, note: Note):
        if note.owner_id:
            user = self.db['Users'].find_one({"id": note.owner_id})
            if not user:
                raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
        if note.send_to_id:
            user = self.db['Users'].find_one({"id": note.send_to_id})
            if not user:
                raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
        result = self.db['Notes'].insert_one(note.dict())
        if result.inserted_id:
            return {"message": "Note sent successfully", "status_code": HTTPStatus.CREATED}
        else:
            raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Error sending note")
    
    def get_all_my_notes(self, owner_id: str):
        notes = self.db['Notes'].find({"owner_id": owner_id})
        return [Note(**note) for note in notes]
    
    def get_all_notes_for_me(self, send_to: str):
        notes = self.db['Notes'].find({"send_to_id": send_to})
        return [Note(**note) for note in notes]
    



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
    # msg = db_instance.change_profile_picture(user.id, "new_profile2.jpg")
    # print(msg)
    msg = db_instance.validate_user("user1", "password123")
    # print(msg)
    annoucement = Annoucement(
        title="Title",
        abstract="Abstract",
        full_text="Full text",
        tags=["Languages"],
        owner="John Doe",
        owner_id=user.id,
        owner_picture="profile.jpg",
        owner_type="Student",
        views=0,
        when_added="10/11/2021",
        location="Warsaw",
        is_active=True,
        working_type="FullTime",
        level_of_experience="Entry",
        requirements=["Python", "Java"]
    )
    # msg = db_instance.add_annoucement(annoucement)
    # print(msg)
    annoucements = db_instance.get_all_annoucements()
    for annoucement in annoucements:
        # print(annoucement.title)
        annoucement_id = annoucement.id

    annoucement = db_instance.get_annoucement(annoucement_id)
    # print(annoucement.dict())

    tags = db_instance.get_all_tags()
    # print(tags)

    note = Note(
        title="Title",
        content="Content",
        owner="John Doe",
        owner_id=user.id,
        owner_picture="profile.jpg",
        send_to="Jane Doe",
        send_to_id=user.id,
        accepted=False
    )
    msg = db_instance.send_note(note)
    print(msg)
    notes = db_instance.get_all_my_notes(user.id)
    for note in notes:
        print(note.title)
    
    notes = db_instance.get_all_notes_for_me(user.id)
    for note in notes:
        print(note.title)
    
