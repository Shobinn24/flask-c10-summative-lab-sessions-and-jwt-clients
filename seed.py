# seed.py
# This file populates the database with fake starter data for testing.
# Run this file directly with: python seed.py
# It uses the Faker library to generate realistic looking fake data
# so we don't have to manually type test data.

from faker import Faker
from config import create_app, db
from models import User, Workout

# Create a Faker instance -- this gives us access to fake data generators
# like fake.name(), fake.sentence(), fake.date() etc.
fake = Faker()

# Create the app so we have access to the database
app = create_app()

def seed_database():
    # We need the app context to interact with the database
    # Without this, SQLAlchemy doesn't know which app/database to use
    with app.app_context():

        # --- Clear Existing Data ---
        # We delete in this order because Workout depends on User (foreign key)
        # If we deleted User first, the database would complain about
        # orphaned Workout records that reference deleted users
        print("Clearing existing data...")
        Workout.query.delete()
        User.query.delete()
        db.session.commit()

        # --- Create Fake Users ---
        print("Creating users...")
        users = []

        # Create one user with known credentials so we can easily test login
        known_user = User(username="testuser")
        known_user.password = "password123"  # Triggers our password setter to hash it
        db.session.add(known_user)
        users.append(known_user)

        # Create 4 more users with random fake data
        for _ in range(4):
            user = User(username=fake.user_name())
            user.password = "password123"  # Same password for easy testing
            db.session.add(user)
            users.append(user)

        # Commit users first so they get their IDs assigned
        # We need those IDs before we can create workouts
        db.session.commit()
        print(f"{len(users)} users created")

        # --- Create Fake Workouts ---
        print("Creating workouts...")

        # List of realistic workout titles to randomly choose from
        workout_titles = [
            "Morning Run",
            "Leg Day",
            "Upper Body Strength",
            "HIIT Session",
            "Yoga Flow",
            "Cycling",
            "Core Circuit",
            "Full Body Workout"
        ]

        # Create 5 workouts for each user
        for user in users:
            for _ in range(5):
                workout = Workout(
                    # fake.random_element() picks a random item from a list
                    title=fake.random_element(workout_titles),

                    # fake.sentence() generates a random sentence
                    # nb_words=10 means roughly 10 words long
                    description=fake.sentence(nb_words=10),

                    # fake.random_int() generates a random integer in a range
                    # duration between 20 and 90 minutes
                    duration=fake.random_int(min=20, max=90),

                    # fake.date_this_year() generates a random date from this year
                    # .strftime formats it as "YYYY-MM-DD" string
                    date=fake.date_this_year().strftime("%Y-%m-%d"),

                    # Associate each workout with its owner
                    user_id=user.id
                )
                db.session.add(workout)

        # Save all workouts to the database
        db.session.commit()
        print(f"{len(users) * 5} workouts created")

        print("Database seeded successfully!")
        print("Test login credentials: username=testuser, password=password123")

# Only runs when you execute this file directly with "python seed.py"
# Won't run if another file imports seed.py
if __name__ == "__main__":
    seed_database()
