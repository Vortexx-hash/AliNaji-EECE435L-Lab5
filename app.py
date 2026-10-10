"""Lab 5 Flask API, using the existing SQLite database functions."""

from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.exceptions import BadRequest, HTTPException

import database

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
database.create_db_table()

USER_FIELDS = ("name", "email", "phone", "address", "country")


def read_user(include_id=False):
    """Validate a complete JSON user before calling the database functions."""
    user = request.get_json()
    if not isinstance(user, dict):
        raise BadRequest("The JSON body must be an object.")

    for field in USER_FIELDS:
        if field not in user or not isinstance(user[field], str) or not user[field].strip():
            raise BadRequest(f"{field} must be a non-empty string.")

    if include_id:
        user_id = user.get("user_id")
        if type(user_id) is not int or user_id < 1:
            raise BadRequest("user_id must be a positive integer.")

    return user


@app.errorhandler(HTTPException)
def api_error(error):
    response = error.get_response()
    response.data = app.json.dumps({"error": error.description})
    response.content_type = "application/json"
    return response


@app.route("/api/users", methods=["GET"])
def api_get_users():
    return jsonify(database.get_users())


@app.route("/api/users/<int:user_id>", methods=["GET"])
def api_get_user(user_id):
    user = database.get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user)


@app.route("/api/users/add", methods=["POST"])
def api_add_user():
    user = database.insert_user(read_user())
    if not user:
        return jsonify({"error": "Cannot add user"}), 500
    # Keep the handout's 200 status for successful CRUD requests.
    return jsonify(user)


@app.route("/api/users/update", methods=["PUT"])
def api_update_user():
    user = read_user(include_id=True)
    if not database.get_user_by_id(user["user_id"]):
        return jsonify({"error": "User not found"}), 404
    updated_user = database.update_user(user)
    if not updated_user:
        return jsonify({"error": "Cannot update user"}), 500
    return jsonify(updated_user)


@app.route("/api/users/delete/<int:user_id>", methods=["DELETE"])
def api_delete_user(user_id):
    if not database.get_user_by_id(user_id):
        return jsonify({"error": "User not found"}), 404
    message = database.delete_user(user_id)
    if message.get("status") != "User deleted successfully":
        return jsonify(message), 500
    return jsonify(message)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
