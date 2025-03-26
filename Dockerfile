FROM apache/airflow:2.7.3

USER root

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER airflow

# Copy requirements.txt and install Python dependencies
COPY requirements.txt /tmp/
RUN pip install --no-cache-dir --user -r /tmp/requirements.txt

# Copy the .env file into the container
COPY .env /opt/airflow/.env

# Copy the config directory into the container
COPY config /opt/airflow/config

# Copy the templates directory into the container
COPY templates /opt/airflow/templates

# Copy the us_visa directory
COPY us_visa /opt/airflow/us_visa

# Copy the main.py file into the container
COPY main.py /opt/airflow/main.py  

# Set PYTHONPATH
ENV PYTHONPATH "${PYTHONPATH}:/opt/airflow"

