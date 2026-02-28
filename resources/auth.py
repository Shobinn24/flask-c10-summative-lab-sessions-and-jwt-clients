# resources/auth.py
# This file handles all authentication routes.
# Signup, Login, and Me (check current user) are defined here.
# These are the routes the frontend will hit first before accessing any workouts.

from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import (
    create_access_token,  # Generates a JWT token for a user
    jwt_required,         # Decorator that protects a route -- requires valid token
    get_jwt_identity      # Extracts the user's id from the token
)
from config import db, bcrypt
from models import User

class Signup(Resource):
    def post(self):
        # Get the JSON data sent in the request body
        data = request.get_json()

        # Make sure username and password were actually provided
        if not data.get("username") or not data.get("password"):
            return {"error": "Username and password are required"}, 400

        # Check if a user with this username already exists in the database
        # .first() returns the first match or None if no match found
        existing_user = User.query.filter_by(username=data["username"]).first()
        if existing_user:
            return {"error": "Username already taken"}, 409  # 409 = Conflict

        # Create a new User instance
        # Setting user.password triggers our password setter in models.py
        # which automatically hashes it before storing
        user = User(username=data["username"])
        user.password = data["password"]

        # Add the new user to the database session and commit (save) it
        db.session.add(user)
        db.session.commit()

        # Create a JWT token for the new user
        # identity is what gets stored inside the token -- we use the user's id
        # so we can look them up later when they make requests
        access_token = create_access_token(identity=str(user.id))

        # Return the token and basic user info
        # 201 = Created, which is the correct status code when something new is made
        return {
            "access_token": access_token,
            "user": {
                "id": user.id,
                "username": user.username
            }
        }, 201


class Login(Resource):
    def post(self):
        data = request.get_json()

        # Make sure both fields were provided
        if not data.get("username") or not data.get("password"):
            return {"error": "Username and password are required"}, 400

        # Look up the user by username in the database
        user = User.query.filter_by(username=data["username"]).first()

        # check_password() hashes the input and compares it to the stored hash
        # If user doesn't exist OR password doesn't match, return same error
        # We intentionally use the same error message for both cases
        # so attackers can't tell whether the username or password was wrong
        if not user or not user.check_password(data["password"]):
            return {"error": "Invalid username or password"}, 401  # 401 = Unauthorized

        # Password matched -- generate a token for this user
        access_token = create_access_token(identity=str(user.id))

        return {
            "access_token": access_token,
            "user": {
                "id": user.id,
                "username": user.username
            }
        }, 200  # 200 = OK


class Me(Resource):
    # jwt_required() protects this route.
    # If the request doesn't include a valid token, Flask returns 401 automatically.
    # The frontend uses this route on page refresh to check if the user is still logged in.
    @jwt_required()
    def get(self):
        # get_jwt_identity() reads the user id we stored inside the token at login
        user_id = get_jwt_identity()

        # Look up the user in the database using that id
        user = User.query.get(user_id)

        if not user:
            return {"error": "User not found"}, 404

        return {
            "id": user.id,
            "username": user.username
        }, 200
