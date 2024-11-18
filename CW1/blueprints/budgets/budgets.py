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
  for budget in budgets.find() .skip(page_start).limit(page_size):
      budget['_id'] = str(budget['_id'])
      for expense in budget['expenses']:
            expense['_id'] = str(expense['_id'])
      for review in budget['reviews']:
        review['_id'] = str(review['_id'])
      data_to_return.append(budget)
      
  return make_response( jsonify(data_to_return), 200 )


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
      return make_response( jsonify( budget), 200 )##gets budget id
  else:
    return make_response( jsonify( { "error" : "Invalid budget ID" } ), 404 )


@budgets_bp.route("/api/v1.0/budgets", methods=["POST"])
@jwt_required
def add_budget():
  if "username" in request.form and "monthly_income" in request.form:
     new_budget = {
            "username": request.form["username"],
            "monthly_income": float(request.form["monthly_income"]),
            "expenses": [],
            "savings": {"goal": 0, "current": 0, "progress": 0},
            "reviews": [],
            "location": {
                "type": "Point",
                "coordinates": [
                    float(request.form.get("latitude", 0)),
                    float(request.form.get("longitude", 0))
                ]
            },
            "town": request.form.get("town", "")
    }
     new_budget_id = budgets.insert_one(new_budget)
     new_budget_link = "http://localhost:5001/api/v1.0/budgets/"+ str(new_budget_id.inserted_id)
     return make_response( jsonify( {"url": new_budget_link} ), 201)
  else:
     return make_response( jsonify({"error":"Missing form data"} ), 404)
  

@budgets_bp.route("/api/v1.0/budgets/<string:id>", methods=["PUT"])
@jwt_required
@admin_required
def edit_budget(id):
    if "username" in request.form and "monthly_income" in request.form:
        update_fields = {
            "username": request.form["username"],
            "monthly_income": float(request.form["monthly_income"]),
            "savings.goal": float(request.form.get("savings_goal", 0)),
            "savings.current": float(request.form.get("savings_current", 0)),
            "savings.progress": float(request.form.get("savings_progress", 0)),
            "location": {
                "type": "Point",
                "coordinates": [
                    float(request.form.get("latitude", 0)),
                    float(request.form.get("longitude", 0))
                ]
            },
            "town": request.form.get("town", "")
        }
        result = budgets.update_one({"_id": ObjectId(id)}, {"$set": update_fields})
        if result.matched_count == 1:
            edited_budget_link = f"http://localhost:5001/api/v1.0/budgets/{id}"
            return make_response(jsonify({"url": edited_budget_link}), 200)
        else:
            return make_response(jsonify({"error": "Invalid budget ID"}), 404)
    else:
        return make_response(jsonify({"error": "Missing form data"}), 400)


@budgets_bp.route("/api/v1.0/budgets/<string:id>", methods=["DELETE"])
@jwt_required
@admin_required
def delete_budget(id):
   result = budgets.delete_one( { "_id" : ObjectId(id) } )
   if result.deleted_count == 1:
      return make_response( jsonify( {} ), 204)
   else:
      return make_response( jsonify( { "error" : "Invalid budget ID" } ), 404)