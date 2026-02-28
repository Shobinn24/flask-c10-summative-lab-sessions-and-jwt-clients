# config.py
# This file sets up our Flask app and all its extensions.
# We use the Application Factory Pattern, which means we define the app
# inside a function (create_app) instead of at the module level.
# This makes it easier to test and scale later.

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

# We initialize extensions WITHOUT the app here.
# This is intentional -- we bind them to the app later inside create_app().
# This pattern prevents circular imports and allows the app to be 
# created multiple times with different configs (useful for testing).
db = SQLAlchemy()       # Handles all database interactions
migrate = Migrate()     # Handles database schema migrations
bcrypt = Bcrypt()       # Handles password hashing
jwt = JWTManager()      # Handles JWT token creation and verification

def create_app():
    # Create the Flask app instance
    app = Flask(__name__)

    # --- App Configuration ---
    # Tell SQLAlchemy to use a local SQLite database file called workout.db
    # SQLite is file-based, so no separate database server is needed
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///workout.db"
    
    # Disable a Flask-SQLAlchemy feature that tracks object modifications
    # We turn this off because it uses extra memory and we don't need it
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    # This secret key is used to sign JWT tokens.
    # When a user logs in, we create a token signed with this key.
    # When they send the token back, we use this key to verify it's legitimate.
    # In a real app, this would be stored in an environment variable, not hardcoded.
    app.config["JWT_SECRET_KEY"] = "super-secret-key"

    # --- Bind Extensions to the App ---
    # Now that the app exists, we connect each extension to it.
    # init_app() is the standard way to do this with the factory pattern.
    db.init_app(app)           # SQLAlchemy now knows which app/db to use
    migrate.init_app(app, db)  # Migrate needs both the app and db to track schema changes
    bcrypt.init_app(app)       # Bcrypt is ready to hash passwords
    jwt.init_app(app)          # JWTManager is ready to create/verify tokens

    # Return the fully configured app so other files can use it
    return app