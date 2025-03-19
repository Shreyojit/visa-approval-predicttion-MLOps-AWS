import logging
import os
from datetime import datetime

# Manually define the project root if from_root() is failing
try:
    from from_root import from_root
    project_root = from_root()  # Try using from_root()
except FileNotFoundError:
    project_root = os.getcwd()  # Fallback to current working directory

LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
log_dir = os.path.join(project_root, "logs")
logs_path = os.path.join(log_dir, LOG_FILE)

# Ensure log directory exists
os.makedirs(log_dir, exist_ok=True)

# Set up logging configuration
logging.basicConfig(
    filename=logs_path,
    format="[ %(asctime)s ] %(name)s - %(levelname)s - %(message)s",
    level=logging.DEBUG,
)

# Test logging
logging.info("Logging system initialized successfully.")
