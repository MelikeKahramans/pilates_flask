import os

class Config:
    SECRET_KEY = os.urandom(24)
    SQLALCHEMY_DATABASE_URI = 'mysql://admin:Kahraman.55@localhost/pilates_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
