from datetime import datetime
import logging
from airflow import DAG
from airflow.operators.python import PythonOperator
from us_visa.entity.artifact_entity import (DataIngestionArtifact, DataValidationArtifact, 
                                           DataTransformationArtifact, ModelTrainerArtifact,
                                           ModelEvaluationArtifact, ModelPusherArtifact)
from us_visa.pipeline.training_pipeline import TrainPipeline

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 1, 1),
    'retries': 1,
}

pipeline = TrainPipeline()  # Initialize once

def data_ingestion(**kwargs):
    try:
        artifact = pipeline.start_data_ingestion()
        kwargs['ti'].xcom_push(key='data_ingestion', value=artifact.__dict__)
        logging.info("Data Ingestion completed successfully.")
    except Exception as e:
        logging.error(f"Data Ingestion failed: {e}")
        raise

def data_validation(**kwargs):
    try:
        ti = kwargs['ti']
        data = ti.xcom_pull(task_ids='data_ingestion', key='data_ingestion')
        artifact = DataIngestionArtifact(**data)

        val_artifact = pipeline.start_data_validation(artifact)
        ti.xcom_push(key='data_validation', value=val_artifact.__dict__)
        logging.info("Data Validation completed successfully.")
    except Exception as e:
        logging.error(f"Data Validation failed: {e}")
        raise

def data_transformation(**kwargs):
    try:
        ti = kwargs['ti']
        ing_data = ti.xcom_pull(task_ids='data_ingestion', key='data_ingestion')
        ing_artifact = DataIngestionArtifact(**ing_data)

        val_data = ti.xcom_pull(task_ids='data_validation', key='data_validation')
        val_artifact = DataValidationArtifact(**val_data)

        trans_artifact = pipeline.start_data_transformation(ing_artifact, val_artifact)
        ti.xcom_push(key='data_transformation', value=trans_artifact.__dict__)
        logging.info("Data Transformation completed successfully.")
    except Exception as e:
        logging.error(f"Data Transformation failed: {e}")
        raise

def model_trainer(**kwargs):
    try:
        ti = kwargs['ti']
        trans_data = ti.xcom_pull(task_ids='data_transformation', key='data_transformation')
        trans_artifact = DataTransformationArtifact(**trans_data)

        model_artifact = pipeline.start_model_trainer(trans_artifact)
        ti.xcom_push(key='model_trainer', value=model_artifact.__dict__)
        logging.info("Model Training completed successfully.")
    except Exception as e:
        logging.error(f"Model Training failed: {e}")
        raise

def model_evaluation(**kwargs):
    try:
        ti = kwargs['ti']
        ing_data = ti.xcom_pull(task_ids='data_ingestion', key='data_ingestion')
        ing_artifact = DataIngestionArtifact(**ing_data)

        model_data = ti.xcom_pull(task_ids='model_trainer', key='model_trainer')
        model_artifact = ModelTrainerArtifact(**model_data)

        eval_artifact = pipeline.start_model_evaluation(ing_artifact, model_artifact)
        ti.xcom_push(key='model_evaluation', value=eval_artifact.__dict__)
        logging.info("Model Evaluation completed successfully.")
    except Exception as e:
        logging.error(f"Model Evaluation failed: {e}")
        raise

def model_pusher(**kwargs):
    try:
        ti = kwargs['ti']
        eval_data = ti.xcom_pull(task_ids='model_evaluation', key='model_evaluation')
        eval_artifact = ModelEvaluationArtifact(**eval_data)

        pusher_artifact = pipeline.start_model_pusher(eval_artifact)
        ti.xcom_push(key='model_pusher', value=pusher_artifact.__dict__)
        logging.info("Model Pusher completed successfully.")
    except Exception as e:
        logging.error(f"Model Pusher failed: {e}")
        raise

with DAG(
    'us_visa_approval',
    default_args=default_args,
    schedule_interval='@weekly',
    catchup=False
) as dag:

    ingestion = PythonOperator(
        task_id='data_ingestion',
        python_callable=data_ingestion,
        provide_context=True
    )

    validation = PythonOperator(
        task_id='data_validation',
        python_callable=data_validation,
        provide_context=True
    )

    transformation = PythonOperator(
        task_id='data_transformation',
        python_callable=data_transformation,
        provide_context=True
    )

    trainer = PythonOperator(
        task_id='model_trainer',
        python_callable=model_trainer,
        provide_context=True
    )

    evaluator = PythonOperator(
        task_id='model_evaluation',
        python_callable=model_evaluation,
        provide_context=True
    )

    pusher = PythonOperator(
        task_id='model_pusher',
        python_callable=model_pusher,
        provide_context=True
    )

    ingestion >> validation >> transformation >> trainer >> evaluator >> pusher
