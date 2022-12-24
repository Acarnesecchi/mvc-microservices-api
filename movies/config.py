import os

class Config:
    SECRET_KEY = os.urandom(32)
    basedir = os.path.abspath(os.path.dirname(__file__))
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://alex:changeme@localhost:5432/prac3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
