from flask import Blueprint, request, make_response, jsonify
from bson import ObjectId
from decorators import jwt_required, admin_required
import globals

reviews_bp = Blueprint("reviews_bp", __name__)

budgets = globals.db.budgets

#ADD A NEW REVIEW
@reviews_bp.route("/api/v1.0/budgets/<string:id>/reviews", methods=["POST"])
@jwt_required
def add_new_review(id):
   new_review = {
      "_id" : ObjectId(),#PROVIDES A UNIQUE ID FOR THE REVIEW
      "username" : request.form["username"],
      "comment" : request.form["comment"],
      "stars" : request.form["stars"]
      }
   budgets.update_one( { "_id" : ObjectId(id) }, { 
      "$push": { "reviews" : new_review } 
      } )
   new_review_link = "http://localhost:5001/api/v1.0/budgets/" \
    + id +"/reviews/" + str(new_review['_id'])
   return make_response( jsonify( { "url" : new_review_link } ), 201 )

#GET A REVIEW
@reviews_bp.route("/api/v1.0/budgets/<string:id>/reviews", methods=["GET"])
def fetch_all_reviews(id):
   data_to_return = []
   budget = budgets.find_one( { "_id" : ObjectId(id) }, { "reviews" : 1, "_id" : 0 } )
   if budget is None:
        return make_response(jsonify({"error": "Invalid budget ID"}), 404)
   for review in budget["reviews"]:
    review["_id"] = str(review["_id"])
    data_to_return.append(review)
   return make_response( jsonify( data_to_return ), 200 )


@reviews_bp.route("/api/v1.0/budgets/<bid>/reviews/<rid>", methods=["GET"])
def fetch_one_review(bid, rid):
   budget = budgets.find_one({ "reviews._id" : ObjectId(rid) },{ 
      "_id" : 0, "reviews.$" : 1 
      } )
   if budget is None:
      return make_response(jsonify({"error":"Invalid budget ID or review ID"}),404)
   budget['reviews'][0]['_id'] =str(budget['reviews'][0]['_id'])
   return make_response( jsonify( budget['reviews'][0]), 200)


@reviews_bp.route("/api/v1.0/budgets/<bid>/reviews/<rid>", methods=["PUT"])
@jwt_required
def edit_review(bid, rid):
   edited_review = {
      "reviews.$.username" : request.form["username"],
      "reviews.$.comment" : request.form["comment"],
      "reviews.$.stars" : request.form['stars']
      }
   budgets.update_one( { 
      "reviews._id" : ObjectId(rid) 
      }, { 
         "$set" : edited_review } )
   edited_review_url = "http://localhost:5001/api/v1.0/budgets/" \
      + bid + "/reviews/" + rid
   return make_response( jsonify( {"url":edit_review_url} ), 200)



@reviews_bp.route("/api/v1.0/budgets/<bid>/reviews/<rid>", methods=["DELETE"])
@jwt_required
@admin_required
def delete_review(bid, rid):
  budgets.update_one(
     { "_id" : ObjectId(bid) },
     {"$pull" : { "reviews" : { "_id" : ObjectId(rid) } } }
  )
  return make_response( jsonify( {} ), 204)