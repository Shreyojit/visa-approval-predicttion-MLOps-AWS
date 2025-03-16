import os
import sys
import numpy as np
import mlflow
import mlflow.sklearn
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from neuro_mf import ModelFactory

from us_visa.exception import USvisaException
from us_visa.logger import logging
from us_visa.utils.main_utils import load_numpy_array_data, load_object, save_object
from us_visa.entity.config_entity import ModelTrainerConfig
from us_visa.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact, ClassificationMetricArtifact
from us_visa.entity.estimator import USvisaModel

# Set up DagsHub credentials for MLflow tracking
dagshub_token = os.getenv("CAPSTONE_TEST")
if not dagshub_token:
    raise EnvironmentError("CAPSTONE_TEST environment variable is not set")

os.environ["MLFLOW_TRACKING_USERNAME"] = dagshub_token
os.environ["MLFLOW_TRACKING_PASSWORD"] = dagshub_token

MLFLOW_TRACKING_URI = "https://dagshub.com/vikashdas770/YT-Capstone-Project.mlflow"
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

class ModelTrainer:
    def __init__(self, data_transformation_artifact: DataTransformationArtifact,
                 model_trainer_config: ModelTrainerConfig):
        self.data_transformation_artifact = data_transformation_artifact
        self.model_trainer_config = model_trainer_config

    def get_model_object_and_report(self, train: np.array, test: np.array):
        try:
            logging.info("Finding the best model using ModelFactory")
            model_factory = ModelFactory(model_config_path=self.model_trainer_config.model_config_file_path)
            x_train, y_train, x_test, y_test = train[:, :-1], train[:, -1], test[:, :-1], test[:, -1]

            best_model_detail = model_factory.get_best_model(
                X=x_train, y=y_train, base_accuracy=self.model_trainer_config.expected_accuracy
            )
            model_obj = best_model_detail.best_model

            y_pred = model_obj.predict(x_test)
            metrics = {
                "accuracy": accuracy_score(y_test, y_pred),
                "f1_score": f1_score(y_test, y_pred),
                "precision": precision_score(y_test, y_pred),
                "recall": recall_score(y_test, y_pred),
            }
            metric_artifact = ClassificationMetricArtifact(**metrics)

            return best_model_detail, metric_artifact
        except Exception as e:
            raise USvisaException(e, sys) from e

    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        logging.info("Starting model training process")
        try:
            train_arr = load_numpy_array_data(self.data_transformation_artifact.transformed_train_file_path)
            test_arr = load_numpy_array_data(self.data_transformation_artifact.transformed_test_file_path)

            with mlflow.start_run():
                best_model_detail, metric_artifact = self.get_model_object_and_report(train=train_arr, test=test_arr)
                preprocessing_obj = load_object(self.data_transformation_artifact.transformed_object_file_path)

                if best_model_detail.best_score < self.model_trainer_config.expected_accuracy:
                    raise Exception("No suitable model found with required accuracy")

                usvisa_model = USvisaModel(
                    preprocessing_object=preprocessing_obj,
                    trained_model_object=best_model_detail.best_model
                )
                save_object(self.model_trainer_config.trained_model_file_path, usvisa_model)

                mlflow.log_params({
                    "expected_accuracy": self.model_trainer_config.expected_accuracy,
                    "best_model": str(type(best_model_detail.best_model).__name__),
                })
                mlflow.log_metrics(metric_artifact.__dict__)
                mlflow.sklearn.log_model(best_model_detail.best_model, "model")

                model_trainer_artifact = ModelTrainerArtifact(
                    trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                    metric_artifact=metric_artifact,
                )
                return model_trainer_artifact
        except Exception as e:
            raise USvisaException(e, sys) from e
