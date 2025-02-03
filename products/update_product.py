import os

import requests
from fastapi import Depends, FastAPI
from fastapi.security import HTTPAuthorizationCredentials
from pymongo import MongoClient

from auth.jwt_token import security, verify_jwt

app = FastAPI()
client = MongoClient(os.environ["MONGODB_URI"])
db = client["digikala"]
products_collection = db["products"]

@app.get("/fetch_products")
def fetch_products(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    verify_jwt(token)

    response = requests.get("https://seller.digikala.com/api/v2/products/seller")
    if response.status_code != 200:
        return {"message": "An error occurred"}
    
    data = response.json().get("data", [])
    if data:
        products = data.get("items", [])
        
        for product in products:
            try:
                existing_product = products_collection.find_one({"id": product["id"]})
                if existing_product:
                    products_collection.update_one({"id": product["id"]}, {"$set": product})
                else:
                    products_schema = ["id", "title", "market_price", "status"]
                    products_collection.insert_one({key: product[key] for key in products_schema})
            except Exception as e:
                return {"message": f"An error occurred: {e}"}
    
    return {"message": "Products inserted/updated"}