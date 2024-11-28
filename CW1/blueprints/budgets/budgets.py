from flask import Blueprint, request, make_response, jsonify
from bson import ObjectId
from decorators import jwt_required, admin_required
import globals
import string #for checking hex digits in the id

budgets_bp = Blueprint("budgets_bp", __name__)

budgets = globals.db.budgets # select the collection name

@budgets_bp.route("/api/v1.0/budgets", methods=["GET"])
def show_all_budgets():
    page_num, page_size = 1, 10
    if request.args.get('pn'):
        page_num = int(request.args.get('pn'))
    if request.args.get('ps'):
        page_size = int(request.args.get('ps'))
    page_start = (page_size * (page_num - 1))
    
    data_to_return = []
    for budget in budgets.find().skip(page_start).limit(page_size):
        budget['_id'] = str(budget['_id'])
        for expense in budget['expenses']:
            expense['_id'] = str(expense['_id'])
        for review in budget['reviews']:
            review['_id'] = str(review['_id'])
        # Reorder fields
        ordered_budget = {
            "_id": budget['_id'],
            "username": budget['username'],
            "monthly_income": budget['monthly_income'],
            "expenses": budget['expenses'],
            "savings": budget['savings'],
            "town": budget['town'],
            "location": budget['location'],
            "reviews": budget['reviews']
        }
        data_to_return.append(ordered_budget)
    
    return make_response(jsonify(data_to_return), 200)


@budgets_bp.route("/api/v1.0/budgets/<string:id>", methods=['GET'])
@jwt_required
def show_one_budget(id):
  if len(id) != 24 or not all(c in string.hexdigits for c in id):
    return make_response( jsonify( { "error" : "Invalid budget ID" } ), 404 )#checks if the id is valid
  budget = budgets.find_one({'_id':ObjectId(id)})
  if budget is not None:
      budget['_id'] = str(budget['_id'])
      for expense in budget['expenses']:
            expense['_id'] = str(expense['_id'])
      for review in budget['reviews']:
          review['_id'] = str(review['_id']) #converts the object id to string
         # Reorder fields
      ordered_budget = {
         "_id": budget['_id'],
         "username": budget['username'],
         "monthly_income": budget['monthly_income'],
         "expenses": budget['expenses'],
         "savings": budget['savings'],
         "town": budget['town'],
         "location": budget['location'],
         "reviews": budget['reviews']
        }
      return make_response( jsonify( budget), 200 )##gets budget id
  else:
    return make_response( jsonify( { "error" : "Invalid budget ID" } ), 404 )


@budgets_bp.route("/api/v1.0/budgets", methods=["POST"])
@jwt_required
def add_budget():
    try:
        if "username" not in request.form or "monthly_income" not in request.form:
            return make_response(jsonify({"error": "Missing form data"}), 400)
        
        username = request.form["username"]
        monthly_income = float(request.form["monthly_income"])
        town = request.form.get("town", "")
        latitude = float(request.form.get("latitude", 0))
        longitude = float(request.form.get("longitude", 0))
        
        new_budget = {
            "username": username,
            "monthly_income": monthly_income,
            "expenses": [],
            "savings": {"goal": 0, "current": 0, "progress": 0},
            "town": town,
            "location": {
                "type": "Point",
                "coordinates": [latitude, longitude]
            },
            "reviews": []
        }
        new_budget_id = budgets.insert_one(new_budget).inserted_id
        new_budget_link = f"http://localhost:5001/api/v1.0/budgets/{new_budget_id}"
        return make_response(jsonify({"url": new_budget_link}), 201)
    except ValueError:
        return make_response(jsonify({"error": "Invalid data type"}), 400)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)
  

@budgets_bp.route("/api/v1.0/budgets/<string:id>", methods=["PUT"])
@jwt_required
@admin_required
def edit_budget(id):
    try:
        if "username" not in request.form or "monthly_income" not in request.form:
            return make_response(jsonify({"error": "Missing form data"}), 400)
        
        username = request.form["username"]
        monthly_income = float(request.form["monthly_income"])
        savings_goal = float(request.form.get("savings_goal", 0))
        savings_current = float(request.form.get("savings_current", 0))
        savings_progress = float(request.form.get("savings_progress", 0))
        town = request.form.get("town", "")
        latitude = float(request.form.get("latitude", 0))
        longitude = float(request.form.get("longitude", 0))
        
        update_fields = {
            "username": username,
            "monthly_income": monthly_income,
            "savings.goal": savings_goal,
            "savings.current": savings_current,
            "savings.progress": savings_progress,
            "town": town,
            "location": {
                "type": "Point",
                "coordinates": [latitude, longitude]
            }
        }
        result = budgets.update_one({"_id": ObjectId(id)}, {"$set": update_fields})
        if result.matched_count == 1:
            edited_budget_link = f"http://localhost:5001/api/v1.0/budgets/{id}"
            return make_response(jsonify({"url": edited_budget_link}), 200)
        else:
            return make_response(jsonify({"error": "Invalid budget ID"}), 404)
    except ValueError:
        return make_response(jsonify({"error": "Invalid data type"}), 400)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)


@budgets_bp.route("/api/v1.0/budgets/<string:id>", methods=["DELETE"])
@jwt_required
@admin_required
def delete_budget(id):
   result = budgets.delete_one( { "_id" : ObjectId(id) } )
   if result.deleted_count == 1:
      return make_response( jsonify( {} ), 204)
   else:
      return make_response( jsonify( { "error" : "Invalid budget ID" } ), 404)