import secrets


class Config:
    SECRET_KEY = secrets.token_hex(24)
    SQLALCHEMY_DATABASE_URI = "sqlite:///site.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
