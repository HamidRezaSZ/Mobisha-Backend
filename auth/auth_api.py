import os

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient

from auth.jwt_token import create_jwt_token

app = FastAPI()

client = MongoClient(os.environ["MONGODB_URI"])
db = client["digikala"]
users_collection = db["users"]

class LoginData(BaseModel):
    username: str
    password: str

@app.post("/login")
def login(data: LoginData):
    user = users_collection.find_one({"username": data.username})
    if user and user["password"] == data.password:
        token = create_jwt_token({"sub": data.username})
        return {"message": "Login successful", "token": token}
    raise HTTPException(status_code=401, detail="Invalid credentials")