import sys
import os
from dotenv import load_dotenv


from us_visa.exception import USvisaException
from us_visa.logger import logging
from us_visa.components.data_ingestion import DataIngestion
from us_visa.components.data_validation import DataValidation
from us_visa.components.data_transformation import DataTransformation
from us_visa.entity.config_entity import (DataIngestionConfig, DataValidationConfig,DataTransformationConfig)
from us_visa.entity.artifact_entity import (DataIngestionArtifact, DataValidationArtifact,DataTransformationArtifact)


class TrainPipeline:
    def __init__(self):
        try:
            logging.info("Initializing TrainPipeline...")
            self.data_ingestion_config = DataIngestionConfig()
            self.data_validation_config = DataValidationConfig()
            self.data_transformation_config = DataTransformationConfig()
        except Exception as e:
            raise USvisaException(e, sys) from e

    def start_data_ingestion(self) -> DataIngestionArtifact:
        """
        Starts the data ingestion component.
        """
        try:
            logging.info("Starting data ingestion...")
            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info("Data ingestion completed successfully.")
            return data_ingestion_artifact
        except Exception as e:
            if isinstance(e, USvisaException):
                raise e
            raise USvisaException(e, sys) from e

    def start_data_validation(self, data_ingestion_artifact: DataIngestionArtifact) -> DataValidationArtifact:
        """
        Starts the data validation component.
        """
        try:
            logging.info("Starting data validation...")
            data_validation = DataValidation(
                data_ingestion_artifact=data_ingestion_artifact,
                data_validation_config=self.data_validation_config
            )
            data_validation_artifact = data_validation.initiate_data_validation()
            logging.info("Data validation completed successfully.")
            return data_validation_artifact
        except Exception as e:
            raise USvisaException(e, sys) from e
        
    def start_data_transformation(self, data_ingestion_artifact: DataIngestionArtifact, data_validation_artifact: DataValidationArtifact) -> DataTransformationArtifact:
        """
        This method of TrainPipeline class is responsible for starting data transformation component
        """
        try:
            data_transformation = DataTransformation(data_ingestion_artifact=data_ingestion_artifact,
                                                     data_transformation_config=self.data_transformation_config,
                                                     data_validation_artifact=data_validation_artifact)
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            return data_transformation_artifact
        except Exception as e:
            raise USvisaException(e, sys)
            

    def run_pipeline(self) -> None:
        """
        Runs the complete training pipeline.
        """
        try:
            logging.info("Running the training pipeline...")
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact)
            data_transformation_artifact = self.start_data_transformation(
                data_ingestion_artifact=data_ingestion_artifact, data_validation_artifact=data_validation_artifact)
            logging.info("Training pipeline executed successfully.")
        except Exception as e:
            if isinstance(e, USvisaException):
                raise e
            raise USvisaException(e, sys)


def main():
    """
    Main function to execute the training pipeline.
    """
    try:
        logging.info("Starting TrainPipeline execution...")
        pipeline = TrainPipeline()
        pipeline.run_pipeline()
        logging.info("TrainPipeline execution finished successfully.")
    except Exception as e:
        logging.error(f"Pipeline failed: {str(e)}")
        if isinstance(e, USvisaException):
            raise e
        raise USvisaException(e, sys)


if __name__ == "__main__":
    main()
