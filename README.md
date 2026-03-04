# Club Registration System (Backend)
This is a Flask-based backend API for managing student club registrations.

The system allows students to:
- View available clubs
- Take a club-specific quiz
- Register for a club only if they pass the quiz

The focus of this project is backend structure, validation logic, and database integrity.
This project was built to practice building a clean and reliable REST API without focusing on frontend components.

---

## Tech Stack
- Python (Flask)
- PostgreSQL
- psycopg2
- python-dotenv
- Logging using RotatingFileHandler

---

## Key Features
- Modular structure using Flask Blueprints
- Quiz-based eligibility before registration
- Database-level constraint to prevent duplicate registrations  
  (A student cannot register for the same club twice)
- Structured logging for tracking important events
- Environment-based configuration using `.env`
  
---

## API Endpoints

GET `/api/clubs`  
GET `/api/quiz/<club_id>`  
POST `/api/quiz/submit`  
POST `/api/register`

Tested using Postman.

---

## How to Run

1. Clone the repository
2. Create a virtual environment
3. Install requirements:

   pip install -r requirements.txt

4. Create a `.env` file with database credentials
5. Run:

   python app.py

Server runs on: http://127.0.0.1:5000
