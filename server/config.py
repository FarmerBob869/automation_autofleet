import os


class Config:
    DEBUG = False
    TESTING = False
    MONGO_HOST = os.getenv('MONGO_HOST', 'localhost')
    MONGO_PORT = int(os.getenv('MONGO_PORT', '27017'))
    MONGO_USERNAME = os.getenv('MONGO_USERNAME', 'root')
    MONGO_PASSWORD = os.getenv('MONGO_PASSWORD', 'password')
    MONGO_DB_NAME = os.getenv('MONGO_DATABASE', 'testdb')
    MONGO_URI = os.getenv('MONGO_URI') or f"mongodb://{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB_NAME}"
    URL = "https://qatask.netlify.app/"