import os

from pymongo import MongoClient

from celery import Celery

celery_app = Celery('tasks', broker='pyamqp://guest@localhost//')
client = MongoClient(os.environ["MONGODB_URI"])
db = client["digikala"]
products_collection = db["products"]
price_history_collection = db["price_history"]

@celery_app.task
def log_price_change(id, old_price, new_price, result):
    try:
        price_history_collection.insert_one({
            "id": id,
            "old_price": old_price,
            "new_price": new_price,
            "timestamp": result["timestamp"],
            "status": result["status"],
            "response": result
        })
    except Exception as e:
        return f"An error occurred: {e}"