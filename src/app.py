import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from api import api


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    CORS(app)

    app.register_blueprint(api, url_prefix=f"/")

    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({"status": 404, "success": False, "message": "Not Found."}), 404

    @app.errorhandler(500)
    def server_error(error):
        return (
            jsonify({"status": 500, "success": False, "message": "Server Error."}),
            500,
        )

    return app


APP = create_app()

if __name__ == "__main__":
    APP.run(host="0.0.0.0", port=8080, debug=True)
