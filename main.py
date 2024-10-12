from db import DB
from fastapi import FastAPI
from models.user_model import User, UserInDB
from models.annoucement_model import Annoucement
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
db = DB()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/create_user")
async def create_user(user: UserInDB):
    return db.create_new_user(user)

@app.get("/get_user/{username}")
async def get_user(username: str):
    return db.get_user(username)

@app.get("/get_user_id/{user_id}")
async def get_user_id(user_id: str):
    return db.get_user_id(user_id)

@app.put("/change_profile_picture/{user_id}")
async def change_profile_picture(user_id: str, profile_picture: str):
    return db.change_profile_picture(user_id, profile_picture)

@app.post("/validate_user/{username}/{password}")
async def validate_user(username: str, password: str):
    return db.validate_user(username, password)

@app.post("/add_annoucement")
async def add_annoucement(annoucement: Annoucement):
    return db.add_annoucement(annoucement)

@app.get('/get_annoucement_owner/{owner}')
async def get_annoucement_owner(owner: str):
    return db.get_annoucement_owner(owner)

@app.get('/get_annoucements')
async def get_all_annoucements():
    return db.get_all_annoucements()

@app.get('/get_annoucement_id/{annoucement_id}')
async def get_annoucement_id(annoucement_id: str):
    return db.get_annoucement_id(annoucement_id)




@app.get('/kleksik')
async def kleksik():
    return {"message": "kleksik"}