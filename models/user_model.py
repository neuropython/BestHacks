from enum import Enum
from pydantic import BaseModel, Field
from typing import List
import bcrypt
import secrets


class Tags(str, Enum):
    Infromatics = "Informatics"
    Mathematics = "Mathematics"
    Physics = "Physics"
    Chemistry = "Chemistry"
    Biology = "Biology"
    History = "History"
    Philosophy = "Philosophy"
    Literature = "Literature"
    Art = "Art"
    Music = "Music"
    Sports = "Sports"
    Logistics = "Logistics"
    Economics = "Economics"
    Business = "Business"
    Marketing = "Marketing"
    Management = "Management"
    Psychology = "Psychology"
    Sociology = "Sociology"
    Law = "Law"
    Medicine = "Medicine"
    Engineering = "Engineering"
    Architecture = "Architecture"
    Design = "Design"
    Languages = "Languages"
    Other = "Other"
    Building = "Building"
    Agriculture = "Agriculture"
    Environment = "Environment"
    Politics = "Politics"
    Religion = "Religion"
    Technology = "Technology"
    Science = "Science"
    Social = "Social"
    Culture = "Culture"
    Food = "Food"
    Health = "Health"
    Fashion = "Fashion"
    Travel = "Travel"
    Electronics = "Electronics"
    Mechanics = "Mechanics"
    Robotics = "Robotics"
    Automation = "Automation"
    Biomedical = "Biomedical"
    Nanotechnology = "Nanotechnology"
    Energy = "Energy"
    Education = "Education"
    Space = "Space"
    Military = "Military"
    Security = "Security"
    

class UserType(str, Enum):
    Student = "Student"
    Teacher = "Teacher"
    Professional = "Professional"

class User(BaseModel):
    id : str = secrets.token_hex(nbytes=16)
    name: str
    second_name: str
    bio: str
    tags: List[Tags]
    email: str
    username: str
    profile_picture: str
    how_many_requests: int
    user_type: UserType
    academical_index: str

class UserInDB(User):
    password: str

    def __init__(self, **data):
        super().__init__(**data)
        self.password = self.hash_password(data['password'])

    @staticmethod
    def hash_password(password: str) -> str:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

