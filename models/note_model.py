from pydantic import BaseModel
from typing import Optional
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
    accepted: Optional[bool] = None

class NoteInDB(Note):
    accepted: bool = False

    def __init__(self, **data):
        super().__init__(**data)
        if self.owner_id[0] == '"':
            self.owner_id = self.owner_id[1:-1]
        if self.send_to_id[0] == '"':
            self.send_to_id = self.send_to_id[1:-1]    
        user = db['Users'].find_one({"id": str(self.owner_id)})
        self.owner = user['username']
        self.owner_picture = user['profile_picture']
        sender = db['Users'].find_one({"id": self.send_to_id})
        self.send_to = sender["username"]