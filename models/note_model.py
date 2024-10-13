from pydantic import BaseModel
from typing import Optional
import datetime
from config import ConnecttoDB

db = ConnecttoDB().connect()

class Note(BaseModel):
    title: str
    content: str
    owner_id: str 
    send_to_id: str 
    owner: Optional[str] = None
    owner_picture: Optional[str] = None
    send_to: Optional[str] = None
    accepted: bool

class NoteInDB(Note):
    def __init__(self, **data):
        super().__init__(**data)
        user = db['Users'].find_one({"id": self.owner_id})
        self.owner = user['username']
        self.owner_picture = user['profile_picture']
        sender = db['Users'].find_one({"id": self.send_to_id})
        self.send_to = sender["username"]