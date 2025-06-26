import logging
import json
import sys
from datetime import datetime
import os

# Ensure logs directory exists
os.makedirs('logs', exist_ok=True)


# Set up the main app logger
app_logger = logging.getLogger('app_logger')
app_logger.setLevel(logging.INFO)
app_logger.propagate = False  # Prevent propagation to root logger

app_handler = logging.FileHandler('logs/app.log')
app_formatter = logging.Formatter('[%(asctime)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
app_handler.setFormatter(app_formatter)
app_logger.addHandler(app_handler)

# Set up the prediction logger
prediction_logger = logging.getLogger('prediction_logger')
prediction_logger.setLevel(logging.INFO)
prediction_logger.propagate = False  # Prevent propagation

prediction_handler = logging.FileHandler('logs/prediction_log.txt')
prediction_handler.setFormatter(app_formatter)
prediction_logger.addHandler(prediction_handler)

# Set up the error logger
error_logger = logging.getLogger('error_logger')
error_logger.setLevel(logging.ERROR)
error_logger.propagate = False  # Prevent propagation

error_handler = logging.FileHandler('logs/error_log.txt')
error_handler.setFormatter(app_formatter)
error_logger.addHandler(error_handler)

def log_prediction(post, prediction, config):
    if not config.get("log_predictions", False):
        return
    prediction_logger.info(f"Input: {post} | Prediction: {prediction}")

def log_error(error_type, input_data, message):
    error_logger.error(f"{error_type} | Input: {input_data} | Message: {message}")



