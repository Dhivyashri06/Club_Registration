from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)
CORS(app)

def connect_db():
    return psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="spotify",
        host="localhost",
        port="5432"
    )

@app.route("/clubs", methods=["GET"])
def get_clubs():
    conn = connect_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute("SELECT id, name, description FROM clubs")
    clubs = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify(clubs)

@app.route("/quiz/<int:club_id>", methods=["GET"])
def get_quiz(club_id):
    conn = connect_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute("""
        SELECT id, question, option_a, option_b
        FROM questions
        WHERE club_id = %s
        ORDER BY id
    """, (club_id,))

    questions = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify(questions)

@app.route("/quiz/submit", methods=["POST"])
def submit_quiz():
    data = request.get_json()

    club_id = data["club_id"]
    answers = data["answers"]

    conn = connect_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute("""
        SELECT correct_option
        FROM questions
        WHERE club_id = %s
        ORDER BY id
    """, (club_id,))

    questions = cur.fetchall()

    score = 0
    for i, q in enumerate(questions):
        if answers[i].lower() == q["correct_option"]:
            score += 1
    cur.close()
    conn.close()

    return jsonify({
        "score": score,
        "passed": score >= 3
    })

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    club_id = data["club_id"]
    answers = data["answers"]

    conn = connect_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute("""
        SELECT correct_option
        FROM questions
        WHERE club_id = %s
        ORDER BY id
    """, (club_id,))

    questions = cur.fetchall()

    score = 0
    for i, q in enumerate(questions):
        if answers[i].strip().lower() == q["correct_option"]:
            score += 1

    if score < 3:
        cur.close()
        conn.close()
        return jsonify({"error": "Must pass quiz to register"}), 403

    cur.execute("""
        INSERT INTO students (name, roll_no, course, email, batch, year, club_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        data["name"],
        data["roll_no"],
        data["course"],
        data["email"],
        data["batch"],
        data["year"],
        club_id
    ))

    conn.commit()

    cur.close()
    conn.close()

    return jsonify({"message": "Registration successful!"})

if __name__ == "__main__":
    app.run(debug=True)
