from db import DB
from fastapi import FastAPI
from models.user_model import User, UserInDB
from models.note_model import Note, NoteInDB
from models.annoucement_model import Annoucement, AnnoucementInDb
from fastapi.middleware.cors import CORSMiddleware
from search_eninges import SearchEngines, SearchEnginesEnum
 
app = FastAPI()
db = DB()
filters = SearchEngines()

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
async def add_annoucement(annoucement: AnnoucementInDb):
    return db.add_annoucement(annoucement)

@app.get('/get_annoucement_owner/{owner}')
async def get_annoucement_owner(owner: str):
    return db.get_annoucement_owner(owner)

@app.get('/get_annoucements')
async def get_all_annoucements():
    return db.get_all_annoucements()

@app.get('/get_annoucement/{annoucement_id}')
async def get_annoucement(annoucement_id: str):
    return db.get_annoucement(annoucement_id)

@app.get('/get_all_tags')
async def get_all_tags():
    return db.get_all_tags()

@app.post('/send_note')
async def send_note(note:NoteInDB): 
    return db.send_note(note)

@app.get('/get_all_my_notes/{owner_id}')
async def get_all_my_notes(owner_id: str):
    return db.get_all_my_notes(owner_id)

@app.get('/get_all_notes_for_me/{send_to_id}')
async def get_all_notes_for_me(send_to_id: str):
    return db.get_all_notes_for_me(send_to_id)

@app.get('/search/{search_type}/{search_query}')
async def search(search_type:SearchEnginesEnum, search_query: str):
    return filters.search(search_type,search_query)


@app.get('/nigalink/georgedroid/{george}/fenta/{fenta}')
async def kleksik():
    return {"message": "kleksik"}