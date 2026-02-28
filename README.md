# Workout Log API

A secure RESTful Flask API for tracking personal workouts. Users can register,
log in, and manage their own workout entries. Built with Flask, SQLAlchemy,
and JWT authentication.

---

## Tech Stack

- Python / Flask
- Flask-RESTful
- Flask-SQLAlchemy
- Flask-JWT-Extended
- Flask-Bcrypt
- Flask-Migrate
- SQLite

---

## Installation

1. Clone the repository
   git clone https://github.com/Shobinn24/flask-c10-summative-lab-sessions-and-jwt-clients.git
   cd flask-c10-summative-lab-sessions-and-jwt-clients

2. Install dependencies
   pipenv install

3. Activate the virtual environment
   pipenv shell

4. Initialize the database
   flask db init
   flask db migrate -m "initial migration"
   flask db upgrade

5. Seed the database with fake data
   python seed.py

---

## Running the App

   python app.py

The server will start at http://localhost:5000

Test login credentials from the seed file:
   username: testuser
   password: password123

---

## API Endpoints

### Auth

| Method | Endpoint  | Description                          | Protected |
|--------|-----------|--------------------------------------|-----------|
| POST   | /signup   | Register a new user, returns token   | No        |
| POST   | /login    | Log in, returns token                | No        |
| GET    | /me       | Get current logged in user           | Yes       |

### Workouts

| Method | Endpoint          | Description                        | Protected |
|--------|-------------------|------------------------------------|-----------|
| GET    | /workouts         | Get all workouts for current user  | Yes       |
| POST   | /workouts         | Create a new workout               | Yes       |
| PATCH  | /workouts/<id>    | Update a workout by ID             | Yes       |
| DELETE | /workouts/<id>    | Delete a workout by ID             | Yes       |

---

## Pagination

The GET /workouts endpoint supports pagination via a query parameter.

   GET /workouts?page=1

Response includes:
- workouts: list of workout objects
- page: current page number
- total_pages: total number of pages
- total_workouts: total number of workouts

---

## Request and Response Examples

### POST /signup
Request body:
   {
     "username": "shobinn",
     "password": "mypassword"
   }

Response:
   {
     "access_token": "<jwt_token>",
     "user": { "id": 1, "username": "shobinn" }
   }

### POST /workouts
Request body:
   {
     "title": "Morning Run",
     "description": "5 mile run around the park",
     "duration": 45,
     "date": "2026-02-28"
   }

Response:
   {
     "id": 1,
     "title": "Morning Run",
     "description": "5 mile run around the park",
     "duration": 45,
     "date": "2026-02-28"
   }

---

## Security

- Passwords are hashed using bcrypt and never stored in plain text
- All workout routes require a valid JWT token in the Authorization header
- Users can only view and modify their own workouts
- Unauthorized access returns a 403 Forbidden response

---

## Seeding the Database

Running python seed.py will:
- Clear all existing data
- Create 5 users including one with known credentials
- Create 5 workouts per user (25 total)

Known test credentials:
   username: testuser
   password: password123