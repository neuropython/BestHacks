from pydantic import BaseModel
from typing import List
from models.user_model import Tags

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
    title: str
    abstract: str
    full_text: str
    tags: List[Tags]
    owner: str
    owner_id: str
    owner_picture: str
    owner_type: str
    views: int
    when_added: str
    location : str
    is_active: bool
    working_type: WorkingType
    Level_of_experience: str
    requirements: List[str]
    

