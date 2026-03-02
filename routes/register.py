from flask import Blueprint, jsonify, request
from db import get_cursor

register_bp = Blueprint("register", __name__)

@register_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    required_fields = ["name", "roll_no", "course", "email", "batch", "year", "club_id", "answers"]

    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"{field} is required"}), 400

    conn, cur = get_cursor()

    try:
        # Check quiz result
        cur.execute("""
            SELECT correct_option
            FROM questions
            WHERE club_id = %s
            ORDER BY id;
        """, (data["club_id"],))

        questions = cur.fetchall()

        score = 0
        for i, q in enumerate(questions):
            if i < len(data["answers"]) and data["answers"][i].lower() == q["correct_option"]:
                score += 1

        if score < 3:
            return jsonify({"error": "Must pass quiz to register"}), 403

        # Insert student
        cur.execute("""
            INSERT INTO students (name, roll_no, course, email, batch, year, club_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
        """, (
            data["name"],
            data["roll_no"],
            data["course"],
            data["email"],
            data["batch"],
            data["year"],
            data["club_id"]
        ))

        conn.commit()

        return jsonify({"message": "Registration successful!"}), 201

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()
