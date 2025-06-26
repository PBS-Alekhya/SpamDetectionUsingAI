# author : P.B.S.Alekhya


import joblib
import json
import numpy as np
import os
from app.logger import log_prediction, app_logger
from pydantic import ValidationError
from app.config_validator import ConfigSchema

# Define paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model", "model.joblib")
CONFIG_PATH = os.path.join(BASE_DIR, "..", "config.json")

# Load config from config.json
def load_config():
    if not os.path.exists(CONFIG_PATH):
        app_logger.error("config.json not found. App will crash.")
        raise SystemExit("config.json not found. Exiting.")

    with open(CONFIG_PATH, "r") as f:
        try:
            config_data = json.load(f)
            validated_config = ConfigSchema(**config_data)
            app_logger.info("Config loaded and validated successfully.")
            return validated_config.dict()
        except json.JSONDecodeError:
            app_logger.error("config.json is not a valid JSON file. App will crash.")
            raise SystemExit("config.json is not a valid JSON file. Exiting.")
        except ValidationError as e:
            app_logger.error(f"config.json failed schema validation: {e}")
            raise SystemExit("Invalid config.json structure. Exiting.")

def load_model():
    if not os.path.exists(MODEL_PATH):
        app_logger.error("model.joblib not found in /app/model.")
        raise FileNotFoundError("model.joblib not found in /app/model.")

    app_logger.info("Model loaded successfully.")
    return joblib.load(MODEL_PATH)

def predict_label(post, model, config):
    if not hasattr(model, "predict_proba"):
        app_logger.error("Loaded model does not support predict_proba().")
        raise RuntimeError("Loaded model does not support predict_proba().")

    try:
        probas = model.predict_proba([post])[0]
    except Exception as e:
        app_logger.error(f"Model failed during prediction: {e}")
        raise RuntimeError(f"Model failed during prediction: {e}")

    label_not_spam = config["labels"][0]
    label_spam = config["labels"][1]

    spam_prob = probas[1]
    not_spam_prob = probas[0]

    if spam_prob >= config["confidence_threshold"]:
        label = label_spam
        confidence = spam_prob
    else:
        label = label_not_spam
        confidence = not_spam_prob

    pred_res = {
        "label": label,
        "confidence": round(confidence, 4)
    }

    log_prediction(post, pred_res, config)
    return pred_res
