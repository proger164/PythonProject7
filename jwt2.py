from flask import Flask
from flask import jsonify
from flask import request

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "super-secret"
jwt = JWTManager(app)

@app.route("/login", methods=["POST"])
def login():
    login = request.json.get("login", None)
    password = request.json.get("password", None)
    if login != "user" or password != "pass":
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=login)
    return jsonify(access_token=access_token)

@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


if __name__ == '__main__':
    app.run(debug=True,host='127.0.0.1',port=8087)