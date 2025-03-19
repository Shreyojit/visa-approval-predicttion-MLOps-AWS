import sys
import logging
from pandas import DataFrame
from sklearn.pipeline import Pipeline
from us_visa.exception import USvisaException

class TargetValueMapping:
    """
    This class is responsible for mapping target values to integers and providing reverse mapping.
    """
    
    def __init__(self):
        # Initialize target value mappings
        self.Certified = 0
        self.Denied = 1

    def _asdict(self):
        """
        Returns the target value mappings as a dictionary.
        """
        return self.__dict__

    def reverse_mapping(self):
        """
        Reverses the target value mapping (i.e., maps integers back to target values).
        """
        mapping_response = self._asdict()
        return dict(zip(mapping_response.values(), mapping_response.keys()))


class USvisaModel:
    """
    This class handles the prediction process using a trained model and a preprocessing pipeline.
    """
    
    def __init__(self, preprocessing_object: Pipeline, trained_model_object: object):
        """
        Initializes the USvisaModel class with a preprocessing pipeline and a trained model.

        :param preprocessing_object: A preprocessing pipeline object.
        :param trained_model_object: A trained machine learning model object.
        """
        self.preprocessing_object = preprocessing_object
        self.trained_model_object = trained_model_object

    def predict(self, dataframe: DataFrame) -> DataFrame:
        """
        Predicts the target values for the given input dataframe.

        This method first transforms the raw input using the preprocessing pipeline and then uses
        the trained model to make predictions.

        :param dataframe: The input dataframe containing features.
        :return: Predictions made by the trained model on the transformed features.
        """
        logging.info("Entered predict method of USvisaModel class")

        try:
            # Transform the raw input using the preprocessing pipeline
            transformed_feature = self.preprocessing_object.transform(dataframe)
            logging.info("Transformed input features")

            # Use the trained model to make predictions
            predictions = self.trained_model_object.predict(transformed_feature)
            logging.info("Made predictions using the trained model")

            return predictions

        except Exception as e:
            # Handle errors and raise a custom exception
            raise USvisaException(e, sys) from e

    def __repr__(self):
        """
        String representation of the class for debugging and logging purposes.
        """
        return f"{type(self.trained_model_object).__name__}()"

    def __str__(self):
        """
        String representation of the class for a user-friendly output.
        """
        return f"{type(self.trained_model_object).__name__}()"
