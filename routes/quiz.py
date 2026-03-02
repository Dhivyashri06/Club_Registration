from flask import Blueprint, jsonify, request
from db import get_cursor

quiz_bp = Blueprint("quiz", __name__)

@quiz_bp.route("/quiz/<int:club_id>", methods=["GET"])
def get_quiz(club_id):
    conn, cur = get_cursor()

    try:
        cur.execute("""
            SELECT id, question, option_a, option_b
            FROM questions
            WHERE club_id = %s
            ORDER BY id;
        """, (club_id,))

        questions = cur.fetchall()
        return jsonify(questions)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()


@quiz_bp.route("/quiz/submit", methods=["POST"])
def submit_quiz():
    data = request.get_json()

    club_id = data.get("club_id")
    answers = data.get("answers")

    if not club_id or not answers:
        return jsonify({"error": "Missing required fields"}), 400

    conn, cur = get_cursor()

    try:
        cur.execute("""
            SELECT correct_option
            FROM questions
            WHERE club_id = %s
            ORDER BY id;
        """, (club_id,))

        questions = cur.fetchall()

        score = 0
        for i, q in enumerate(questions):
            if i < len(answers) and answers[i].lower() == q["correct_option"]:
                score += 1

        return jsonify({
            "score": score,
            "passed": score >= 3
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()
