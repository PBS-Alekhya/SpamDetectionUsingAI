# Author : P.B.S.Alekhya


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.generator import load_model, load_config, predict_label
import traceback
from app.logger import app_logger

# Initialize FastAPI app
app = FastAPI()

logger = app_logger
# Load config and model at startup
try:
    config = load_config()
    model = load_model()
    logger.info("Startup successful: Model and config loaded.")
except Exception as e:
    logger.error("Startup failed", exc_info=True)
    raise SystemExit("App failed to start due to config or model error.")

# Define input schema
class PostInput(BaseModel):
    post: str


# main page
@app.get("/")
def root():
    return {"message": "Welcome to the Spam Detection API"}


@app.post("/predict")
def predict(post_input: PostInput):
    if not post_input.post.strip():  
        raise HTTPException(status_code=400, detail="Post input cannot be empty.")
    try:
        logger.info(f"New prediction request: {post_input.post}")
        result = predict_label(post_input.post, model, config)
        return result
    except Exception as e:
        traceback.print_exc()
        logger.error("Prediction error", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/version")
def version():
    return {
        "model": config.get("model_name", "unknown"),
        "version": config.get("version", "unknown")
    }
