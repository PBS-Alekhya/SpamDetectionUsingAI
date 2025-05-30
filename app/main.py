# Author : P.B.S.Alekhya
# date : 27 May 2025
# # last change: 28 may 2025

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.generator import load_model, load_config, predict_label
import traceback

# Initialize FastAPI app
app = FastAPI()

# Load config and model at startup
try:
    config = load_config()
    model = load_model()
except Exception as e:
    print(" Startup failed:", e)
    raise SystemExit("App failed to start due to config or model error.")

# Define input schema
class PostInput(BaseModel):
    post: str

@app.post("/predict")
def predict(post_input: PostInput):
    try:
        result = predict_label(post_input.post, model, config)
        return result
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/version")
def version():
    return {
        "model": config.get("model_name", "unknown"),
        "version": config.get("version", "unknown")
    }
