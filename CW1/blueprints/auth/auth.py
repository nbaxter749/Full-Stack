from flask import Blueprint, request, make_response, jsonify
import bcrypt
import jwt
import datetime
import globals
from decorators import jwt_required, admin_required

auth_bp = Blueprint("auth_bp", __name__)

users = globals.db.users
blacklist = globals.db.blacklist


#login stage
@auth_bp.route("/api/v1.0/login", methods=["GET"])
def login():
   try:
        auth = request.authorization
        if not auth or not auth.username or not auth.password:
            return make_response(jsonify({"message": "Authentication required"}), 401)
        
        user = users.find_one({'username': auth.username})  # checks if the username is in the database
        if user is None:
            return make_response(jsonify({'message': 'Bad Username'}), 401)
        
        if not bcrypt.checkpw(auth.password.encode('utf-8'), user['password']):  # checks if the password is correct
            return make_response(jsonify({'message': 'Bad password'}), 401)
        
        token = jwt.encode({
            'user': auth.username,  # username is the username
            'admin': user['admin'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }, globals.secret_key, algorithm="HS256")
        
        return make_response(jsonify({'token': token}), 200)
    
   except Exception as e:
       return make_response(jsonify({"error": str(e)}), 500)

@auth_bp.route('/api/v1.0/logout', methods=["GET"])
@jwt_required
def logout():
    try:
        token = request.headers.get('x-access-token')
        if not token:
            return make_response(jsonify({"message": "Token is missing"}), 401)
        
        blacklist.insert_one({"token": token})
        return make_response(jsonify({'message': 'Logout successful'}), 200)
    
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)