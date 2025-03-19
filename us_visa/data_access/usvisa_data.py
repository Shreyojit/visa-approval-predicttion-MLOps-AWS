import sys
import pandas as pd
import numpy as np
from typing import Optional
from us_visa.configuration.mongo_db_connection import MongoDBClient
from us_visa.constants import DATABASE_NAME
from us_visa.exception import USvisaException


class USvisaData:
    """
    A class to export MongoDB collection data as a Pandas DataFrame.
    """

    def __init__(self):
        """
        Initializes a connection to MongoDB using MongoDBClient.
        """
        try:
            self.mongo_client = MongoDBClient(database_name=DATABASE_NAME)
        except Exception as e:
            raise USvisaException(e, sys)

    def export_collection_as_dataframe(self, collection_name: str, database_name: Optional[str] = None) -> pd.DataFrame:
        """
        Fetches a MongoDB collection and converts it into a Pandas DataFrame.

        Args:
            collection_name (str): Name of the MongoDB collection to export.
            database_name (Optional[str]): Optional database name (defaults to the initialized database).

        Returns:
            pd.DataFrame: A DataFrame containing the collection data.

        Raises:
            USvisaException: If there is an error in fetching or processing data.
        """
        try:
            db = self.mongo_client[database_name] if database_name else self.mongo_client.database
            collection = db[collection_name]

            # Convert MongoDB collection to DataFrame
            df = pd.DataFrame(list(collection.find()))

            # Drop the MongoDB _id column if it exists
            df.drop(columns=["_id"], errors="ignore", inplace=True)

            # Replace "na" string values with NaN for consistency
            df.replace({"na": np.nan}, inplace=True)

            return df

        except Exception as e:
            raise USvisaException(e, sys)
