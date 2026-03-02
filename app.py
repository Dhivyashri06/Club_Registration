from flask import Flask, jsonify
from flask_cors import CORS

from config import Config
from routes.clubs import clubs_bp
from routes.quiz import quiz_bp
from routes.register import register_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Enable CORS (can later restrict origins in production)
    CORS(app)

    # Register Blueprints
    app.register_blueprint(clubs_bp, url_prefix="/api")
    app.register_blueprint(quiz_bp, url_prefix="/api")
    app.register_blueprint(register_bp, url_prefix="/api")

    # Health check route
    @app.route("/")
    def health_check():
        return jsonify({
            "status": "success",
            "message": "Club Registration API is running"
        })

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
