from fastapi.testclient import TestClient
from app.main import app
from app.config_validator import ConfigSchema
from pydantic import ValidationError

client = TestClient(app)


def test_missing_post_key():
    response = client.post("/predict", json={"message": "Test"})
    assert response.status_code == 422  # FastAPI validation error for missing required field

def test_non_string_post():
    response = client.post("/predict", json={"post": 12345})
    assert response.status_code == 422  # FastAPI will reject non-string input

def test_config_invalid_labels():
    try:
        ConfigSchema(
            model_name="model",
            version="1.0",
            confidence_threshold=0.5,
            labels=["spam"],  # only one label instead of two
            log_predictions=True
        )
        assert False, "Validation should have failed"
    except ValidationError:
        assert True
