from flask import Flask, jsonify, request
from flask_cors import CORS
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import (JWTManager, create_access_token,
                                get_jwt_identity, jwt_required,
                                set_access_cookies, unset_jwt_cookies)

from models import db, User, RegularUser, Todo

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config['SECRET_KEY'] = 'MySecretKey'
app.config["JWT_SECRET_KEY"] = "super-secret"
app.config["JWT_TOKEN_LOCATION"] = ["cookies", "headers"]

db.init_app(app)
CORS(app)
app.app_context().push()
jwt = JWTManager(app)


# Authentication Routes
@app.route('/login', methods=['POST'])
def login():
  data = request.json
  user = User.query.filter_by(username=data['username']).first()
  if user and user.check_password(data['password']):
    token = create_access_token(identity=data['username'])
    response = jsonify(access_token=token)
    set_access_cookies(response, token)
    return response
  return jsonify(error="Invalid username or password"), 401


@app.route('/logout', methods=['GET'])
def logout():
  response = jsonify(message="Logged out")
  unset_jwt_cookies(response)
  return response


# Protected Route Example
@app.route('/todos', methods=['GET'])
@jwt_required()
def get_todos():
  user = RegularUser.query.filter_by(username=get_jwt_identity()).first()
  if not user:
    return jsonify(error="User not found"), 404
  return jsonify([todo.get_json() for todo in user.todos])


if __name__ == "__main__":
  app.run(host="0.0.0.0", debug=True)
