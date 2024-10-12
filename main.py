from db import DB
from fastapi import FastAPI
from models.user_model import User

app = FastAPI()
db = DB()
app = FastAPI()

@app.post("/create_user")
async def create_user(user: User):
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

