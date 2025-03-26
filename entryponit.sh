#!/bin/bash

# Wait for the database to be ready
until airflow db check; do
  echo "Waiting for database to be ready..."
  sleep 5
done

# Initialize the database
airflow db init

# Create an admin user (if not already created)
airflow users list | grep admin || airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com \
    --password admin

# Start the Airflow service
exec airflow "$@"