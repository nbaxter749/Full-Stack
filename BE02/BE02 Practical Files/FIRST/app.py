from flask import Flask, jsonify, make_response, request
import uuid, random

app = Flask(__name__)
#GENERATING RANDOM TOWN DATA AND SPECIFYS BUSINESS AS A DICTIONARY
businesses = {}
    
def generate_dummy_data():
    towns = ['Coleraine', 'Banbridge', 'Belfast', 'Lisburn', 'Ballymena', 'Derry', 'Newry', 
             'Enniskillen', 'Omagh', 'Ballymoney']
    business_dict = {}
    
    for i in range(100):
        id = str(uuid.uuid1())
        name = "Biz " + str(i)
        town = towns[random.randint(0, len(towns)-1)]
        rating = random.randint(1, 5)
        business_dict[id] = {
            "name" : name,
            "town" : town,
            "rating" : rating,
            "reviews" : {} # left reviews as an empy list
        }
    return business_dict


##business code, get to show all business
@app.route("/api/v1.0/businesses", methods=['GET'])
def show_all_businesses():
    page_num, page_size = 1, 10#start of pagination
    if request.args.get('pn'):
        page_num = int(request.args.get('pn'))
    if request.args.get('ps'):
      page_size = int(request.args.get('ps'))#defining page size and page num. if no numbers are provied 1 and 10 are the default
    page_start = (page_size * (page_num - 1))
    businesses_list = [ {k : v} for k,v in businesses.items() ]#coverting from dictionary to list, there was an extra line bellow this on pdf
    return make_response( jsonify( businesses_list[page_start:page_start + page_size] ), 200 ) #end of pagination
#get business id
@app.route("/api/v1.0/businesses/<string:id>", methods=['GET'])
def show_one_business(id): # GETS ALL BUSINNES
  if id in businesses: #check if id exits before rutning a responce
      return make_response( jsonify( businesses[id] ), 200 )##gets business id
  else:
    return make_response( jsonify( { "error" : "Invalid business ID" } ), 404 ) ##generates error
#add a business start of post method
@app.route("/api/v1.0/businesses", methods=['POST'])
def add_business():
    if "name" in request.form and "town" in request.form and "rating" in request.form: # checks to make sure all filled out
      next_id = str(uuid.uuid1())#generates new id
      new_business = {
          'name' : request.form['name'],
          'town' : request.form['town'],
          'rating' : request.form['rating'],
          'reviews' : {}
      }
      businesses[next_id] = new_business #rather append the business to the list new dictiory id  at that value
      return make_response( jsonify( { next_id : new_business } ), 201 )
    else:
        return make_response( jsonify({ "error" : "Missing form data" } ), 404 ) #returns an error if data is missing
#bellow is how to edit a business
@app.route("/api/v1.0/businesses/<string:id>", methods=['PUT'])
def edit_business(id):
    if id not in businesses:
        return make_response( jsonify( { "error" : "Invalid business ID" } ), 404 ) #returns error if not a valid ID
    else:
        if "name" in request.form and "town" in request.form and "rating" in request.form: #checks all data has been filled in
          businesses[id]['name'] = request.form['name']
          businesses[id]['town'] = request.form['town']
          businesses[id]['rating'] = request.form['rating']
          return make_response( jsonify({ id : businesses[id] } ), 200 )
        else:
            return make_response( jsonify( { "error" : "Missing form data" } ), 404 ) #if missing data error will appear
# bellow delete business
@app.route("/api/v1.0/businesses/<string:id>", methods=['DELETE'])
def delete_business(id):
    if id in businesses: #check valid business id
      del businesses[id]
      return make_response( jsonify( {} ), 200)
    else: return make_response( jsonify( { "error" : "Invalid business ID" } ), 404 ) #if not right invalid id

##start of reviews code


@app.route("/api/v1.0/businesses/<string:id>/reviews",methods=["GET"])
def fetch_all_reviews(id):
    if id in businesses:
        page_num, page_size = 1, 2#start of pagination
        if request.args.get('pn'):
            page_num = int(request.args.get('pn'))
        if request.args.get('ps'):
            page_size = int(request.args.get('ps'))#defining page size and page num. if no numbers are provied 1 and 2 are the default
        page_start = (page_size * (page_num - 1))
        reviews_list = list(businesses[id]["reviews"].values())#coverting from dictionary to listvof review objects
        return make_response( jsonify( reviews_list[page_start:page_start + page_size] ), 200 )# Return paginated reviews
    else:
        return make_response( jsonify( { "error" : "Invalid Business ID"} ), 404)
#add a new review via post

@app.route("/api/v1.0/businesses/<string:id>/reviews",methods=["POST"])
def add_new_review(id):
    if id in businesses:
        if "username" in request.form and "comment" in request.form and "stars" in request.form:
            new_review_id = str(uuid.uuid1())
            new_review = {
                "username" : request.form["username"],
                "comment" : request.form["comment"],
                "stars" : request.form["stars"]
            }
            businesses[id]["reviews"][new_review_id] = new_review
            return make_response( jsonify( {new_review_id : new_review } ), 201 )
        else: 
            return make_response( jsonify( { "error" : "Incomplete Form Data" } ), 404 )
    else:
        return make_response( jsonify( { "error" : "Invalid Business ID"} ), 404)

@app.route("/api/v1.0/businesses/<string:id>/reviews/<string:reviewID>", methods=["GET"])
def fetch_one_review(id, reviewID):
    if id in businesses:
        if reviewID in businesses[id]["reviews"]:
            return make_response( jsonify( businesses[id]["reviews"][reviewID] ), 200)
        else:
            return make_response( jsonify( { "error" : "Invalid Review ID"} ), 404)
    else:
        return make_response( jsonify( { "error" : "Invalid Business ID"} ), 404)

@app.route("/api/v1.0/businesses/<string:id>/reviews/<string:reviewID>", methods=["PUT"])
def edit_review(id, reviewID):
    if id in businesses:
        if reviewID in businesses[id]["reviews"]:
            if "username" in request.form and "comment" in request.form and "stars" in request.form:
                businesses[id]["reviews"][reviewID]["username"] = request.form["username"]
                businesses[id]["reviews"][reviewID]["comment"] = request.form["comment"]
                businesses[id]["reviews"][reviewID]["stars"] = request.form["stars"]
                return make_response( jsonify( { reviewID : businesses[id]["reviews"][reviewID]} ), 200)
            else: 
                return make_response( jsonify( { "error" : "Incomplete Form Data" } ), 404 )
        else:
            return make_response( jsonify( { "error" : "Invalid Review ID"} ), 404)
    else:
        return make_response( jsonify( { "error" : "Invalid Business ID"} ), 404)
#delete a review
@app.route("/api/v1.0/businesses/<string:id>/reviews/<string:reviewID>", methods=["DELETE"])
def delete_review(id, reviewID):
    if id in businesses:
        if reviewID in businesses[id]["reviews"]:
            del businesses[id]["reviews"][reviewID]
            return make_response( jsonify( {} ), 200)
        else:
            return make_response( jsonify( { "error" : "Invalid Review ID"} ), 404)
    else:
        return make_response( jsonify( { "error" : "Invalid Business ID"} ), 404)

if __name__ == "__main__":
    businesses = generate_dummy_data()
    app.run(debug=True)