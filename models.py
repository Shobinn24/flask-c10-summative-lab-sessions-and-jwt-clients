# models.py
# This file defines our database tables as Python classes.
# SQLAlchemy translates these classes into actual database tables.
# Each class = one table, each attribute = one column.

from config import db, bcrypt

class User(db.Model):
    # Tell SQLAlchemy what to name this table in the database
    __tablename__ = "users"

    # --- Columns ---
    id = db.Column(db.Integer, primary_key=True)  # Auto-incrementing unique ID
    
    # nullable=False means this field is required
    # unique=True means no two users can have the same username
    username = db.Column(db.String(80), nullable=False, unique=True)
    
    # We never store the actual password, only a hashed version of it
    # The hash is always the same length regardless of password length
    _password_hash = db.Column(db.String(255), nullable=False)

    # --- Relationship ---
    # This tells SQLAlchemy that one User can have many Workouts
    # backref="user" means we can access a workout's owner by typing workout.user
    # cascade="all, delete-orphan" means if a user is deleted,
    # all their workouts are automatically deleted too
    workouts = db.relationship("Workout", backref="user", cascade="all, delete-orphan")

    # --- Password Property ---
    # @property turns this into a getter -- user.password reads this
    @property
    def password(self):
        # We never want to expose the actual hash
        raise AttributeError("Password is not readable")

    # @password.setter runs when we do user.password = "something"
    @password.setter
    def password(self, plain_text_password):
        # bcrypt.generate_password_hash() scrambles the password into a hash
        # .decode("utf-8") converts it from bytes to a regular string for storage
        self._password_hash = bcrypt.generate_password_hash(plain_text_password).decode("utf-8")

    def check_password(self, plain_text_password):
        # bcrypt.check_password_hash() hashes the input and compares it
        # to the stored hash. Returns True if they match, False if not.
        # We never "unhash" a password -- bcrypt doesn't work that way.
        return bcrypt.check_password_hash(self._password_hash, plain_text_password)

    def __repr__(self):
        # This is just a helpful string representation for debugging
        return f"<User {self.username}>"


class Workout(db.Model):
    __tablename__ = "workouts"

    # --- Columns ---
    id = db.Column(db.Integer, primary_key=True)
    
    # Title of the workout, e.g. "Morning Run" or "Leg Day"
    title = db.Column(db.String(100), nullable=False)
    
    # Description of what the workout involved
    description = db.Column(db.String(500), nullable=False)
    
    # How long the workout lasted in minutes
    duration = db.Column(db.Integer, nullable=False)
    
    # The date the workout was performed, stored as a string e.g. "2026-02-28"
    date = db.Column(db.String(20), nullable=False)

    # --- Foreign Key ---
    # This column stores the id of the user who owns this workout.
    # db.ForeignKey("users.id") links this column to the id column in the users table.
    # This is how SQLAlchemy knows which user owns which workout.
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def __repr__(self):
        return f"<Workout {self.title} by User {self.user_id}>"