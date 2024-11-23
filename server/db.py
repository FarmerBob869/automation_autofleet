from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, PyMongoError
from config import Config
import time
import logging

## Function to initialize MongoDB client with retries
def initialize_mongo_client():
    retries = 5
    while retries > 0:
        try:
            mongo_client = MongoClient(
                host=Config.MONGO_HOST,
                port=Config.MONGO_PORT,
                username=Config.MONGO_USERNAME,
                password=Config.MONGO_PASSWORD,
                serverSelectionTimeoutMS=5000  # 5 seconds timeout
            )
            # Attempt to connect to the server to trigger any connection errors
            mongo_client.server_info()
            logging.info("Connected to MongoDB successfully")
            return mongo_client
        except ServerSelectionTimeoutError as e:
            logging.error(f"Server selection timeout: {e}")
        except PyMongoError as e:
            logging.error(f"Error connecting to MongoDB: {e}")
        retries -= 1
        logging.info(f"Retrying MongoDB connection ({5 - retries}/5)")
        time.sleep(5)
    raise Exception("Failed to connect to MongoDB after several retries")


def write_to_db(collection_name, data):
    try:
        collection = db.get_collection(collection_name)
        result = collection.insert_one(data)
        return {"message": "Data stored successfully", "id": str(result.inserted_id)}
    except PyMongoError as e:
        logging.error(f"Error storing data: {e}")
        return {"error": "An error occurred while storing data"}
    