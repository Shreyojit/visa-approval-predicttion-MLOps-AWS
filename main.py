import logging
import sys
from us_visa.pipeline.training_pipeline import TrainPipeline
from us_visa.exception import USvisaException

def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("training.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    logging.info("Starting the training pipeline...")
    
    try:
        train_pipeline = TrainPipeline()
        train_pipeline.run_pipeline()
        logging.info("Training completed successfully!")
    except Exception as e:
        logging.error(f"Error occurred during training: {e}")
        raise USvisaException(e, sys)

if __name__ == "__main__":
    main()