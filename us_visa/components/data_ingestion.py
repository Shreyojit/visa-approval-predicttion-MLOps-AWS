import os
import sys
import logging
from pandas import DataFrame
from sklearn.model_selection import train_test_split

from us_visa.entity.config_entity import DataIngestionConfig
from us_visa.entity.artifact_entity import DataIngestionArtifact
from us_visa.exception import USvisaException
from us_visa.data_access.usvisa_data import USvisaData


class DataIngestion:
    """
    Handles data ingestion from MongoDB, exporting it into a feature store, and splitting it into train and test sets.
    """

    def __init__(self, data_ingestion_config: DataIngestionConfig = DataIngestionConfig()):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise USvisaException(e, sys) from e

    def export_data_into_feature_store(self) -> DataFrame:
        """
        Exports data from MongoDB to a CSV file.

        Returns:
            DataFrame: Exported data.
        
        Raises:
            USvisaException: If an error occurs during data export.
        """
        try:
            logging.info("Exporting data from MongoDB...")
            usvisa_data = USvisaData()
            dataframe = usvisa_data.export_collection_as_dataframe(
                collection_name=self.data_ingestion_config.collection_name
            )

            logging.info(f"Exported data shape: {dataframe.shape}")

            # Save to feature store
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            os.makedirs(os.path.dirname(feature_store_file_path), exist_ok=True)

            logging.info(f"Saving data to: {feature_store_file_path}")
            dataframe.to_csv(feature_store_file_path, index=False, header=True)

            return dataframe

        except Exception as e:
            raise USvisaException(e, sys) from e

    def split_data_as_train_test(self, dataframe: DataFrame) -> None:
        """
        Splits data into training and testing sets.

        Args:
            dataframe (DataFrame): The dataset to split.

        Raises:
            USvisaException: If an error occurs during data splitting.
        """
        try:
            logging.info("Splitting data into train and test sets...")
            train_set, test_set = train_test_split(
                dataframe, test_size=self.data_ingestion_config.train_test_split_ratio
            )

            logging.info(f"Train shape: {train_set.shape}, Test shape: {test_set.shape}")

            # Create necessary directories
            os.makedirs(os.path.dirname(self.data_ingestion_config.training_file_path), exist_ok=True)

            # Save split data
            train_set.to_csv(self.data_ingestion_config.training_file_path, index=False, header=True)
            test_set.to_csv(self.data_ingestion_config.testing_file_path, index=False, header=True)

            logging.info("Train and test data successfully exported.")

        except Exception as e:
            raise USvisaException(e, sys) from e

    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        """
        Initiates the data ingestion process.

        Returns:
            DataIngestionArtifact: Contains paths to train and test data.

        Raises:
            USvisaException: If an error occurs during data ingestion.
        """
        try:
            logging.info("Starting data ingestion...")

            # Export data
            dataframe = self.export_data_into_feature_store()

            # Split into train and test sets
            self.split_data_as_train_test(dataframe)

            # Create and return the artifact
            data_ingestion_artifact = DataIngestionArtifact(
                trained_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path,
            )

            logging.info(f"Data ingestion completed: {data_ingestion_artifact}")
            return data_ingestion_artifact

        except Exception as e:
            raise USvisaException(e, sys) from e
