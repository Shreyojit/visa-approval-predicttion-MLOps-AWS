import logging
import sys
import argparse
from us_visa.pipeline.training_pipeline import TrainPipeline
from us_visa.pipeline.prediction_pipeline import USvisaData, USvisaClassifier
from us_visa.exception import USvisaException
import pandas as pd

def setup_logging():
    # Set up logging configuration
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("app.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )

def train():
    logging.info("Starting the training pipeline...")

    try:
        # Initialize and run the training pipeline
        train_pipeline = TrainPipeline()
        train_pipeline.run_pipeline()
        logging.info("Training completed successfully!")
    except Exception as e:
        logging.error(f"Error occurred during training: {e}")
        raise USvisaException(e, sys)

def predict():
    try:
        logging.info("Starting batch prediction...")

        # Example input data for prediction
        sample_input = {
            "continent": "Asia",
            "education_of_employee": "Master's",
            "has_job_experience": "Y",
            "requires_job_training": "N",
            "no_of_employees": 500,
            "region_of_employment": "Northeast",
            "prevailing_wage": 80000,
            "unit_of_wage": "Year",
            "full_time_position": "Y",
            "company_age": 10
        }

        # Convert input to DataFrame
        usvisa_data = USvisaData(**sample_input)
        usvisa_df = usvisa_data.get_usvisa_input_data_frame()

        # Load model and predict
        model_predictor = USvisaClassifier()
        prediction = model_predictor.predict(dataframe=usvisa_df)[0]

        # Determine the status based on prediction
        status = "Visa-approved" if prediction == 1 else "Visa Not-Approved"
        logging.info(f"Prediction Result: {status}")

        # Print the result to the console
        print(f"Prediction Result: {status}")

    except Exception as e:
        logging.error(f"Error occurred during prediction: {e}")
        raise USvisaException(e, sys)


if __name__ == "__main__":
    setup_logging()

    # Set up argument parser
    parser = argparse.ArgumentParser(description="US Visa Prediction Pipeline")
    parser.add_argument("mode", choices=["train", "predict"], help="Run training or prediction pipeline")

    args = parser.parse_args()

    # Run the selected mode
    if args.mode == "train":
        train()
    elif args.mode == "predict":
        predict()
