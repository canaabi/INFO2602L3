from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password = db.Column(db.String(120), nullable=False)

  def __init__(self, username, email, password):
    self.username = username
    self.email = email
    self.password = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.password, password)

  def __repr__(self):
    return f'<User {self.username}>'


class RegularUser(User):
  todos = db.relationship('Todo', backref='user', lazy=True)


class Todo(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  text = db.Column(db.String(255), nullable=False)
  done = db.Column(db.Boolean, default=False)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

  def get_json(self):
    return {"id": self.id, "text": self.text, "done": self.done}

  def toggle(self):
    self.done = not self.done
    db.session.commit()
