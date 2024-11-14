from pymongo import MongoClient

client = MongoClient("mongodb://127.0.0.1:27017")
db = client.bizDB
businesses = db.biz

pipeline = [
    { "$match" : { "town" : "Banbridge"} },
    { "$project" : {"town" : 1, "profit" : 1 } }
]

for business in businesses.aggregate(pipeline):
    print( business["town"], str(business['profit'][2]["gross"]) )

db.biz.aggregate([{ "$match" : { "town" : "Banbridge"} }, { "$project" : {"town" : 1, "profit" : 1, "num_employees" : 1 } }, { "$unwind" : "$profit" }, { "$match" : {"num_employees" : { "$gte" : 50 },"profit.gross" : { "$gte" : 0 } } },{ "$sort" : { "profit.gross" : -1 } }, { "$skip" : 2 },{ "$limit" : 3 }])