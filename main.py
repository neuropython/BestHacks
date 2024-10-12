from db import DB
from fastapi import FastAPI
from models.user_model import User

app = FastAPI()

db = DB()
app = FastAPI()