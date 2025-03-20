import sys
import pymongo
import certifi

from us_visa.exception import USvisaException
from us_visa.logger import logging
from us_visa.constants import DATABASE_NAME

class MongoDBClient:
    """
    A class to manage MongoDB connection.
    Establishes a connection to MongoDB and provides access to the specified database.
    """

    client = None  # Class-level client to ensure a single connection instance

    def __init__(self, database_name: str = DATABASE_NAME) -> None:
        """
        Initializes a MongoDB connection and sets up the database.

        Args:
            database_name (str): Name of the MongoDB database to connect to. Defaults to DATABASE_NAME.

        Raises:
            USvisaException: If an error occurs during the connection process.
        """
        try:
            if MongoDBClient.client is None:
                # Hardcoded MongoDB connection string
                mongo_db_url = "mongodb+srv://shreyojitdas95:kingof95@cluster0.s72yp.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

                # Establishing connection with SSL certificate verification
                MongoDBClient.client = pymongo.MongoClient(mongo_db_url, tlsCAFile=certifi.where())

            self.client = MongoDBClient.client
            self.database = self.client[database_name]
            self.database_name = database_name

            logging.info(f"Connected to MongoDB database: {database_name}")

        except Exception as e:
            logging.error(f"Error connecting to MongoDB: {e}")
            raise USvisaException(e, sys)
