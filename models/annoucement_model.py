from pydantic import BaseModel
from typing import List
from models.user_model import Tags
from enum import Enum
import secrets
import datetime
from config import ConnecttoDB

db = ConnecttoDB().connect()

class WorkingType(str, Enum):
    FullTime = "FullTime"
    PartTime = "PartTime"
    Remote = "Remote"
    Hybrid = "Hybrid"
    Internship = "Internship"
    Contract = "Contract"
    Freelance = "Freelance"
    Temporary = "Temporary"
    Volunteer = "Volunteer"
    Other = "Other"

class Level_of_experience(str, Enum):
    Student = "Student"
    Entry = "Entry"
    Mid = "Mid"
    Senior = "Senior"
    Expert = "Expert"
    Other = "Other"

class Annoucement(BaseModel):
    id : str
    title: str
    abstract: str
    full_text: str
    tags: List[Tags]
    owner: str
    owner_id: str
    owner_picture: str
    owner_type: str
    when_added: str
    location : str
    working_type: WorkingType
    level_of_experience: str
    requirements: List[str]

class AnnoucementInDb(Annoucement):
    id : str = secrets.token_hex(nbytes=16) 
    views: int = 0
    is_active: bool = True
    when_added: str = datetime.datetime.now().strftime("%d/%m/%Y")
    owner_picture: str = None
    owner_type: str = None
    owner: str = None

    def __init__(self, **data):
        super().__init__(**data)
        if self.owner_id[0] == '"':
            self.owner_id = self.owner_id[1:-1]
        print(self.owner_id)
        user = db['Users'].find_one({"id": str(self.owner_id)})
        self.owner = user['username']
        self.owner_picture = user['profile_picture']
        self.owner_type = user['user_type']
        
        



    

