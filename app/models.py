from app import db, login_mgr, bcrypt, app
from datetime import datetime
from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer as Serializer


@login_mgr.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="user.jpg")
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship("Post", backref="author", lazy=True)

    def get_reset_token(self):
        secret_key = app.config["SECRET_KEY"].encode("utf-8")
        serializer = Serializer(secret_key)
        return serializer.dumps({"user_id": self.id}, salt="reset-salt")

    @staticmethod
    def verify_reset_token(token):
        secret_key = app.config["SECRET_KEY"].encode("utf-8")
        serializer = Serializer(secret_key)
        try:
            user_id = serializer.loads(token, salt="reset-salt")["user_id"]
        except Exception as e:
            print(f"Error verifying token: {e}")
            return None
        return User.query.get(user_id)


class Post(db.Model):
    post_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"Title: {self.title}\nDate Posted: {self.date_posted}"
