import os
import re

import requests
from pymongo import MongoClient

from celery import Celery
from tasks.insert_log import log_price_change

celery_app = Celery('tasks', broker='pyamqp://guest@localhost//')
client = MongoClient(os.getenv("MONGODB_URI", "mongodb://localhost:27017"))
db = client["digikala"]
products_collection = db["products"]

@celery_app.task
def update_prices():
    products = products_collection.find()
    for product in products:
        try:
            new_price = product["market_price"] * 1.1
            response = requests.post("https://seller.digikala.com/api/v2/products/", json={"id": product["id"], "market_price": new_price})
            result = response.json()
            
            if result["status"] == "success":
                products_collection.update_one({"id": product["id"]}, {"$set": {"market_price": new_price}})
                log_price_change.delay(product["id"], product["market_price"], new_price, result)
        except Exception as e:
            return f"An error occurred: {e}"

    return "Prices updated"