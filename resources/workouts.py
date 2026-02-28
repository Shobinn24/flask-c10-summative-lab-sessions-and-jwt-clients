# resources/workouts.py
# This file handles all workout CRUD routes.
# WorkoutList handles the collection (GET all, POST new).
# WorkoutDetail handles a single workout by ID (PATCH, DELETE).
# All routes are protected -- you must be logged in to access them.

from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from config import db
from models import Workout

class WorkoutList(Resource):

    @jwt_required()
    def get(self):
        # get_jwt_identity() pulls the user's id out of the JWT token
        # This tells us which user is making the request
        user_id = get_jwt_identity()

        # --- Pagination ---
        # The frontend sends a "page" parameter in the URL like /workouts?page=1
        # request.args.get() reads URL query parameters
        # We default to page 1 if no page is specified
        # int() converts the string "1" to the integer 1
        page = int(request.args.get("page", 1))

        # How many workouts to show per page
        per_page = 5

        # --- Filtered and Paginated Query ---
        # We filter by user_id so users only see THEIR workouts
        # .paginate() handles the math of which records to return for each page
        # error_out=False means if someone requests a page that doesn't exist,
        # we get an empty list instead of a 404 error
        paginated = Workout.query.filter_by(user_id=user_id).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )

        # paginated.items contains the actual workout objects for this page
        # We convert each workout to a dictionary so Flask can return it as JSON
        workouts = [
            {
                "id": w.id,
                "title": w.title,
                "description": w.description,
                "duration": w.duration,
                "date": w.date
            }
            for w in paginated.items  # This is a list comprehension -- a compact loop
        ]

        # Return the workouts along with pagination metadata
        # The frontend can use total_pages to know how many pages exist
        return {
            "workouts": workouts,
            "page": page,
            "total_pages": paginated.pages,
            "total_workouts": paginated.total
        }, 200

    @jwt_required()
    def post(self):
        # Get the current user's id from the token
        user_id = get_jwt_identity()

        # Get the JSON data from the request body
        data = request.get_json()

        # Validate that all required fields were provided
        if not data.get("title") or not data.get("description") or \
           not data.get("duration") or not data.get("date"):
            return {"error": "All fields are required"}, 400

        # Create a new Workout instance with the provided data
        # user_id comes from the token, not the request body
        # This is important -- we never trust the client to tell us who they are
        # We always get the user identity from the verified token
        workout = Workout(
            title=data["title"],
            description=data["description"],
            duration=data["duration"],
            date=data["date"],
            user_id=user_id  # Automatically associate with the logged in user
        )

        # Save to the database
        db.session.add(workout)
        db.session.commit()

        return {
            "id": workout.id,
            "title": workout.title,
            "description": workout.description,
            "duration": workout.duration,
            "date": workout.date
        }, 201  # 201 = Created


class WorkoutDetail(Resource):

    @jwt_required()
    def patch(self, id):
        # Get the current user's id from the token
        user_id = get_jwt_identity()

        # Look up the workout by its id in the database
        # .get() returns the workout or None if not found
        workout = Workout.query.get(id)

        # If workout doesn't exist, return 404
        if not workout:
            return {"error": "Workout not found"}, 404

        # CRITICAL SECURITY CHECK
        # We convert both to strings for comparison because
        # get_jwt_identity() returns a string but user_id in db is an integer
        # If the workout belongs to a different user, deny access
        if str(workout.user_id) != str(user_id):
            return {"error": "Unauthorized"}, 403  # 403 = Forbidden

        # Get the updated data from the request body
        data = request.get_json()

        # Update only the fields that were provided in the request
        # This allows partial updates -- you don't have to send all fields
        if "title" in data:
            workout.title = data["title"]
        if "description" in data:
            workout.description = data["description"]
        if "duration" in data:
            workout.duration = data["duration"]
        if "date" in data:
            workout.date = data["date"]

        # Save the changes
        db.session.commit()

        return {
            "id": workout.id,
            "title": workout.title,
            "description": workout.description,
            "duration": workout.duration,
            "date": workout.date
        }, 200

    @jwt_required()
    def delete(self, id):
        user_id = get_jwt_identity()

        workout = Workout.query.get(id)

        if not workout:
            return {"error": "Workout not found"}, 404

        # Same security check as patch -- make sure this workout belongs
        # to the user making the request
        if str(workout.user_id) != str(user_id):
            return {"error": "Unauthorized"}, 403

        # Remove the workout from the database and commit
        db.session.delete(workout)
        db.session.commit()

        # 204 = No Content, which is the correct status code for a successful delete
        # We return an empty string because 204 responses have no body
        return "", 204
