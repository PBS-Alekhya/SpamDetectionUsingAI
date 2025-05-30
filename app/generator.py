# author : P.B.S.Alekhya
# date : 26th May 2025
# last change: 28th May 2025 , 10:24

import joblib
import json
import numpy as np
import os


# Define paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model", "model.joblib")
CONFIG_PATH = os.path.join(BASE_DIR, "..", "config.json")

# Load config from config.json
def load_config():
    if not os.path.exists(CONFIG_PATH):
        raise FileNotFoundError("config.json not found.")
    with open(CONFIG_PATH, "r") as f:
        config = json.load(f)
    if "threshold" not in config or "labels" not in config:
        raise ValueError("config.json is missing required fields.")
    return config

def load_model():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(" model.joblib not found in /app/model.")
    return joblib.load(MODEL_PATH)

# Make prediction using the pipeline model
def predict_label(post, model, config):
    prob = model.predict_proba([post])[0][1]  # Probability of spam (class 1)
    label = config["labels"][0] if prob >= config["threshold"] else config["labels"][1]
    return {
        "Prediction": label,
        "confidence": round(prob, 4)
    }
