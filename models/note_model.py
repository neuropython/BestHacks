from pydantic import BaseModel

class Note(BaseModel):
    title: str
    content: str
    owner: str
    owner_id: str
    owner_picture: str
    send_to: str
    send_to_id: str
    accepted: bool
