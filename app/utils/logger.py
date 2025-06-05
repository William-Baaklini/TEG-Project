import logging
import os

# Ensure logs directory exists
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Create a named logger
logger = logging.getLogger("app")
logger.setLevel(logging.INFO)

if not logger.handlers:
    # File handler
    file_handler = logging.FileHandler(f"{LOG_DIR}/app.log")
    file_handler.setLevel(logging.INFO)

    # Console handler (optional)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
