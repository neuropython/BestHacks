import os
from pymongo import MongoClient
from typing import List
from dotenv import load_dotenv
import datetime
from fastapi import HTTPException
from enum import Enum

load_dotenv()
PASSWORD = os.getenv("password")
USERNAME = os.getenv("user") 

MONGO_URI = f"mongodb+srv://{USERNAME}:{PASSWORD}@hackyeahbackend.ai51i.mongodb.net/?retryWrites=true&w=majority&appName=HackYeahBackend"


class SearchEnginesEnum(str, Enum):
    title = "title"
    owner = "owner"
    tags = "tags"
    location = "location"
    working_type = "working_type"
    level_of_experience = "level_of_experience"
    requirements = "requirements"
    owner_type = "owner_type"
    popularity = "popularity"
    last_added = "last_added"


class SearchEngines:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SearchEngines, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        self.client = MongoClient(MONGO_URI)
        self.db = self.client['BestHacks']

    def search_by_title(self, title: str):
        annoucements = self.db['Annoucements'].find({"title": {"$regex": title, "$options": "i"}})
        if annoucements:
            return [annoucement for annoucement in annoucements]
        else:
            raise HTTPException(status_code=404, detail="Annoucement not found")
    
    def search_by_owner(self, owner: str):
        annoucements = self.db['Annoucements'].find({"owner": {"$regex": owner, "$options": "i"}})
        if annoucements:
            return [annoucement for annoucement in annoucements]
        else:
            raise HTTPException(status_code=404, detail="Annoucement not found")
    
    def search_by_tags(self, tags: List[str]):
        annoucements = self.db['Annoucements'].find({"tags": {"$in": tags}})
        if annoucements:
            return [annoucement for annoucement in annoucements]
        else:
            raise HTTPException(status_code=404, detail="Annoucement not found")
        
    def search_by_location(self, location: str):
        annoucements = self.db['Annoucements'].find({"location": {"$regex": location, "$options": "i"}})
        if annoucements:
            return [annoucement for annoucement in annoucements]
        else:
            return HTTPException(status_code=404, detail="Annoucement not found")
    
    def search_by_working_type(self, working_type: str):
        annoucements = self.db['Annoucements'].find({"working_type": working_type})
        if annoucements:
            return [annoucement for annoucement in annoucements]
        else:
            return HTTPException(status_code=404, detail="Annoucement not found")
    
    def search_by_level_of_experience(self, level_of_experience: str):
        annoucements = self.db['Annoucements'].find({"level_of_experience": level_of_experience})
        if annoucements:
            return [annoucement for annoucement in annoucements]
        else:
            return HTTPException(status_code=404, detail="Annoucement not found")
        
    def search_by_requirements(self, requirements: List[str]):
        annoucements = self.db['Annoucements'].find({"requirements": {"$all": requirements}})
        if annoucements:
            return [annoucement for annoucement in annoucements]
        else:
            return HTTPException(status_code=404, detail="Annoucement not found")
    
    def search_by_owner_type(self, owner_type: str):
        annoucements = self.db['Annoucements'].find({"owner_type": owner_type})
        if annoucements:
            return [annoucement for annoucement in annoucements]
        else:
            return HTTPException(status_code=404, detail="Annoucement not found")
    
    def search_by_last_added(self, when_added: str):
        date = datetime.datetime.strptime(when_added, "%d/%m/%Y")
        annoucements = self.db['Annoucements'].find({"when_added": {"$gte": date}})
        if annoucements:
            return [annoucement for annoucement in annoucements]
        else:
            return HTTPException(status_code=404, detail="Annoucement not found")
        
    def search_by_popularity(self):
        annoucements = self.db['Annoucements'].find().sort("views", -1)
        if annoucements:
            return [annoucement for annoucement in annoucements]
        else:
            return HTTPException(status_code=404, detail="Annoucement not found")
    
    def search(self, search_engine: SearchEnginesEnum, search_value):
        if search_engine == SearchEnginesEnum.title:
            return self.search_by_title(search_value)
        elif search_engine == SearchEnginesEnum.popularity:
            return self.search_by_popularity()
        elif search_engine == SearchEnginesEnum.owner:
            return self.search_by_owner(search_value)
        elif search_engine == SearchEnginesEnum.tags:
            return self.search_by_tags(search_value)
        elif search_engine == SearchEnginesEnum.location:
            return self.search_by_location(search_value)
        elif search_engine == SearchEnginesEnum.working_type:
            return self.search_by_working_type(search_value)
        elif search_engine == SearchEnginesEnum.level_of_experience:
            return self.search_by_level_of_experience(search_value)
        elif search_engine == SearchEnginesEnum.requirements:
            return self.search_by_requirements(search_value)
        elif search_engine == SearchEnginesEnum.owner_type:
            return self.search_by_owner_type(search_value)
        elif search_engine == SearchEnginesEnum.last_added:
            return self.search_by_last_added(search_value)
        else:
            return HTTPException(status_code=404, detail="Search engine not found")
        

if __name__ == "__main__":
    search = SearchEngines()
    results = search.search(SearchEnginesEnum.title, "Title")
    print(results)
    # results = search.search(SearchEnginesEnum.owner, "user1")
    # for result in results:
    #     print(result)
    # results = search.search(SearchEnginesEnum.tags, ["Informatics"])
    # for result in results:
    #     print(result)
    result =search.search(SearchEnginesEnum.location, "Wroclaw")

    # print(search.search(SearchEnginesEnum.working_type, "Python"))
    # print(search.search(SearchEnginesEnum.level_of_experience, "Python"))
    # print(search.search(SearchEnginesEnum.requirements, ["Python"]))
    # print(search.search(SearchEnginesEnum.owner_type, "Python"))
    # print(search.search(SearchEnginesEnum.last_added, "10/10/2021"))