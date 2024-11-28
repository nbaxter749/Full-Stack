from flask import Blueprint, request, make_response, jsonify
from bson import ObjectId
from decorators import jwt_required, admin_required
import globals

reviews_bp = Blueprint("reviews_bp", __name__)

budgets = globals.db.budgets

# ADD A NEW REVIEW
@reviews_bp.route("/api/v1.0/budgets/<string:id>/reviews", methods=["POST"])
@jwt_required
def add_new_review(id):
    try:
        # Validate budget ID
        if len(id) != 24 or not all(c in "0123456789abcdef" for c in id):
            return make_response(jsonify({"error": "Invalid budget ID"}), 400)
        
        # Validate form data
        if "username" not in request.form or "comment" not in request.form or "stars" not in request.form:
            return make_response(jsonify({"error": "Missing form data"}), 400)
        
        username = request.form["username"]
        comment = request.form["comment"]
        stars = int(request.form["stars"])
        
        # Validate stars
        if stars < 1 or stars > 5:
            return make_response(jsonify({"error": "Stars must be between 1 and 5"}), 400)
        
        new_review = {
            "_id": ObjectId(),  # PROVIDES A UNIQUE ID FOR THE REVIEW
            "username": username,
            "comment": comment,
            "stars": stars
        }
        
        # Check if budget exists
        budget = budgets.find_one({"_id": ObjectId(id)})
        if not budget:
            return make_response(jsonify({"error": "Budget not found"}), 404)
        
        budgets.update_one(
            {"_id": ObjectId(id)},
            {"$push": {"reviews": new_review}}
        )
        
        new_review_link = f"http://localhost:5001/api/v1.0/budgets/{id}/reviews/{new_review['_id']}"
        return make_response(jsonify({"url": new_review_link}), 201)
    
    except ValueError:
        return make_response(jsonify({"error": "Invalid data type"}), 400)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)

# GET ALL REVIEWS
@reviews_bp.route("/api/v1.0/budgets/<string:id>/reviews", methods=["GET"])
def fetch_all_reviews(id):
    try:
        # Validate budget ID
        if len(id) != 24 or not all(c in "0123456789abcdef" for c in id):
            return make_response(jsonify({"error": "Invalid budget ID"}), 400)
        
        data_to_return = []
        budget = budgets.find_one({"_id": ObjectId(id)}, {"reviews": 1, "_id": 0})
        if not budget:
            return make_response(jsonify({"error": "Budget not found"}), 404)
        
        for review in budget["reviews"]:
            review["_id"] = str(review["_id"])
            data_to_return.append(review)
        
        return make_response(jsonify(data_to_return), 200)
    
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)

# GET A SINGLE REVIEW
@reviews_bp.route("/api/v1.0/budgets/<string:bid>/reviews/<string:rid>", methods=["GET"])
def fetch_one_review(bid, rid):
    try:
        # Validate budget ID and review ID
        if len(bid) != 24 or not all(c in "0123456789abcdef" for c in bid):
            return make_response(jsonify({"error": "Invalid budget ID"}), 400)
        if len(rid) != 24 or not all(c in "0123456789abcdef" for c in rid):
            return make_response(jsonify({"error": "Invalid review ID"}), 400)
        
        budget = budgets.find_one({"reviews._id": ObjectId(rid)}, {"_id": 0, "reviews.$": 1})
        if not budget:
            return make_response(jsonify({"error": "Invalid budget ID or review ID"}), 404)
        
        budget['reviews'][0]['_id'] = str(budget['reviews'][0]['_id'])
        return make_response(jsonify(budget['reviews'][0]), 200)
    
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)

# EDIT A REVIEW
@reviews_bp.route("/api/v1.0/budgets/<string:bid>/reviews/<string:rid>", methods=["PUT"])
@jwt_required
def edit_review(bid, rid):
    try:
        # Validate form data
        if "username" not in request.form or "comment" not in request.form or "stars" not in request.form:
            return make_response(jsonify({"error": "Missing form data"}), 400)
        
        username = request.form["username"]
        comment = request.form["comment"]
        stars = int(request.form["stars"])
        
        # Validate stars
        if stars < 1 or stars > 5:
            return make_response(jsonify({"error": "Stars must be between 1 and 5"}), 400)
        
        edited_review = {
            "reviews.$.username": username,
            "reviews.$.comment": comment,
            "reviews.$.stars": stars
        }
        
        result = budgets.update_one(
            {"reviews._id": ObjectId(rid)},
            {"$set": edited_review}
        )
        
        if result.matched_count == 1:
            edited_review_link = f"http://localhost:5001/api/v1.0/budgets/{bid}/reviews/{rid}"
            return make_response(jsonify({"url": edited_review_link}), 200)
        else:
            return make_response(jsonify({"error": "Invalid review ID"}), 404)
    
    except ValueError:
        return make_response(jsonify({"error": "Invalid data type"}), 400)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)

# DELETE A REVIEW
@reviews_bp.route("/api/v1.0/budgets/<string:bid>/reviews/<string:rid>", methods=["DELETE"])
@jwt_required
@admin_required
def delete_review(bid, rid):
    try:
        result = budgets.update_one(
            {"_id": ObjectId(bid)},
            {"$pull": {"reviews": {"_id": ObjectId(rid)}}}
        )
        if result.modified_count == 1:
            return make_response(jsonify({}), 204)
        else:
            return make_response(jsonify({"error": "Invalid review ID"}), 404)
    
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)