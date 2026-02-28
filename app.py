# app.py
# This is the entry point of our Flask application.
# It creates the app, registers our routes, and runs the server.
# We keep this file lean -- the heavy lifting happens in config.py and resources/

from flask import Flask
from flask_restful import Api
from config import create_app, db

# Import our resource classes (we'll build these next)
from resources.auth import Signup, Login, Me
from resources.workouts import WorkoutList, WorkoutDetail

# Create the app using our factory function from config.py
app = create_app()

# Flask-RESTful's Api class manages our routes.
# Instead of using @app.route decorators, we register classes with api.add_resource()
api = Api(app)

# --- Register Auth Routes ---
# Each add_resource() call maps a URL path to a Resource class.
# The Resource class defines what happens for GET, POST, DELETE etc on that path.
api.add_resource(Signup, "/signup")        # POST /signup -- create a new user
api.add_resource(Login, "/login")          # POST /login -- authenticate and get token
api.add_resource(Me, "/me")               # GET /me -- get current logged in user

# --- Register Workout Routes ---
# WorkoutList handles the collection -- getting all workouts and creating new ones
api.add_resource(WorkoutList, "/workouts")

# WorkoutDetail handles a single workout by its ID -- update and delete
# <int:id> is a URL parameter, Flask will extract it and pass it to our methods
api.add_resource(WorkoutDetail, "/workouts/<int:id>")

# This block only runs when you execute app.py directly with "python app.py"
# It won't run if another file imports app.py
if __name__ == "__main__":
    # debug=True gives us helpful error messages and auto-reloads on code changes
    # Turn this OFF in production -- it exposes sensitive info
    app.run(debug=True)