import os

from pymongo import MongoClient

os.environ["MONGODB_URI"] = os.getenv("MONGODB_URI", "mongodb://localhost:27017")

try:
    client = MongoClient(os.environ["MONGODB_URI"])
    db = client["digikala"]

    # Users collection
    db.create_collection("users")
    db["users"].create_index("username", unique=True)
    db["users"].insert_one({"username": "test_user", "password": "test_pass"})

    # Products collection
    db.create_collection("products")
    db["products"].create_index("dkpc", unique=True)

    print("Database and collections created successfully")
except Exception as e:
    print(f"An error occurred: {e}")