from pymongo import MongoClient
from bson import ObjectId
import random

client = MongoClient("mongodb://127.0.0.1:27017")
db = client.budgetDB
budgets = db.budgets

# Insert initial data if the collection is empty
if budgets.count_documents({}) == 0:
    budgets.insert_many([
        {
            "username": "john_doe",
            "monthly_income": random.randint(2000, 10000),
            "expenses": [
                {
                    "_id": ObjectId(),
                    "category": "Housing",
                    "amount": random.randint(500, 2000),
                    "date": "2023-11-01",
                    "comment": "Rent payment"
                },
                {
                    "_id": ObjectId(),
                    "category": "Transportation",
                    "amount": random.randint(50, 300),
                    "date": "2023-11-05",
                    "comment": "Gas refill"
                }
            ],
            "savings": {
                "goal": random.randint(5000, 20000),
                "current": random.randint(1000, 5000),
                "progress": random.randint(1, 100)
            },
            "reviews": [
                {
                    "_id": ObjectId(),
                    "username": "user1",
                    "comment": "This is a review",
                    "stars": random.randint(1, 5)
                },
                {
                    "_id": ObjectId(),
                    "username": "user2",
                    "comment": "Another review",
                    "stars": random.randint(1, 5)
                }
            ],
            "location": {
                "type": "Point",
                "coordinates": [
                    random.uniform(-90, 90),  # Latitude
                    random.uniform(-180, 180)  # Longitude
                ]
            },
            "town": "Sample Town"
        }
    ])

# Update existing documents with new fields
for budget in budgets.find():
    budgets.update_one(
        { "_id": budget['_id'] },
        { 
            "$set": { 
                "monthly_income": random.randint(2000, 10000),
                "expenses": [
                    {
                        "_id": ObjectId(),
                        "category": "Housing",
                        "amount": random.randint(500, 2000),
                        "date": "2023-11-01",
                        "comment": "Rent payment"
                    },
                    {
                        "_id": ObjectId(),
                        "category": "Transportation",
                        "amount": random.randint(50, 300),
                        "date": "2023-11-05",
                        "comment": "Gas refill"
                    }
                ],
                "savings": {
                    "goal": random.randint(5000, 20000),
                    "current": random.randint(1000, 5000),
                    "progress": random.randint(1, 100)
                },
                "reviews": [
                    {
                        "_id": ObjectId(),
                        "username": "user1",
                        "comment": "This is a review",
                        "stars": random.randint(1, 5)
                    },
                    {
                        "_id": ObjectId(),
                        "username": "user2",
                        "comment": "Another review",
                        "stars": random.randint(1, 5)
                    }
                ],
                "location": {
                    "type": "Point",
                    "coordinates": [
                        random.uniform(-90, 90),  # Latitude
                        random.uniform(-180, 180)  # Longitude
                    ]
                },
                "town": "Sample Town"
            } 
        }
    )