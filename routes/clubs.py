from flask import Blueprint, jsonify
from db import get_cursor

clubs_bp = Blueprint("clubs", __name__)

@clubs_bp.route("/clubs", methods=["GET"])
def get_clubs():
    conn, cur = get_cursor()

    try:
        cur.execute("SELECT id, name, description FROM clubs ORDER BY id;")
        clubs = cur.fetchall()
        return jsonify(clubs)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()
