from flask import Flask, request, jsonify, make_response
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

client = MongoClient("mongodb://127.0.0.1:27017" )
db = client.bizDB # select the database
businesses = db.biz # select the collection


@app.route("/api/v1.0/businesses", methods=["GET"])
def show_all_businesses():
  page_num, page_size = 1, 10
  if request.args.get('pn'):
    page_num = int(request.args.get('pn'))
  if request.args.get('ps'):
      page_size = int(request.args.get('ps'))
  page_start = (page_size * (page_num - 1))
      
  data_to_return = []
  for business in businesses.find() .skip(page_start).limit(page_size):
      business['_id'] = str(business['_id'])
      for review in business['reviews']:
        review['_id'] = str(review['_id'])
      data_to_return.append(business)
      
  return make_response( jsonify(data_to_return), 200 )


@app.route("/api/v1.0/businesses/<string:id>", methods=['GET'])
def show_one_business(id):
  business = businesses.find_one({'_id':ObjectId(id)})
  if business is not None:
      business['_id'] = str(business['_id'])
      for review in business['reviews']:
          review['_id'] = str(review['_id']) #converts the object id to string
      return make_response( jsonify( business), 200 )##gets business id
  else:
    return make_response( jsonify( { "error" : "Invalid business ID" } ), 404 )


@app.route("/api/v1.0/businesses", methods=["POST"])
def add_business():
  if "name" in request.form and 
  "town" in request.form and
"rating" in request.form:
new_business = {
"name" : request.form["name"],
"town" : request.form["town"],
"rating" : request.form["rating"],
"reviews" : []
}
new_business_id = businesses.insert_one(new_business)
new_business_link = \
"http://localhost:5000/api/v1.0/businesses/" \
+ str(new_business_id.inserted_id)
return make_response( jsonify(
{"url": new_business_link} ), 201)
else:
return make_response( jsonify(
{"error":"Missing form data"} ), 404)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)